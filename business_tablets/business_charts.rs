#!/usr/bin/env rust-script
//! ```cargo
//! [dependencies]
//! plotlib = "0.5.1"
//! ```
use std::fs::File;
use std::io::prelude::*;
use std::collections::HashMap;
use plotlib::repr::BarChart;
use plotlib::view::CategoricalView;
use plotlib::page::Page;

const KINGS: [&'static str; 10] = [
    "Shamash-shum-ukin",
    "Kandalanu",
    "Nabopolassar",
    "Nebuchadnezzar II",
    "Amel-Marduk",
    "Neriglissar",
    "La-bashi-Marduk",
    "Nabonid",
    "Cyrus",
    "Cambyses"
];

fn main() -> std::io::Result<()> {
    let mut file = File::open("CHRON.CHN")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    for k in &KINGS {
        let columns = compute_for_king(k, &contents);
        let max = columns.keys().fold(0, |a, &b| a.max(b));
        let bars: Vec<_> = (0 .. max + 1).map(|year| {
            let count = columns.get(&year).unwrap_or(&0);
            let label = match year {
                0 => "Acc.".to_string(),
                x => format!("{}", x),
            };
            BarChart::new(*count as f64).label(label)
        }).collect();

        let mut view = CategoricalView::new().x_label("Year");
        for bar in bars {
            view = view.add(bar);
        }
        let name = k.to_ascii_lowercase().replace(" ", "_");
        Page::single(&view).save(format!("../src/graphics/{}.svg", name)).unwrap();
    }

    Ok(())
}

fn compute_for_king(king: &str, chn: &str) -> HashMap<u32, u32> {
    let mut map = HashMap::new();
    let mut current_year = None;
    let mut counter: u32 = 0;
    for line in chn.lines() {
        if line.starts_with(format!("{}, year ", king).as_str()) {
            let split: Vec<&str> = line[king.len() - 1..].split_whitespace().collect();
            let year = split.get(2).and_then(|x| x[..x.len() - 1].parse::<u32>().ok());
            if year.is_some() {
                current_year = year;
                counter = 0;
            }
        } else if current_year.is_some() && line.starts_with("Number of texts:") {
            let split: Vec<&str> = line.split_whitespace().collect();
            let number = split.get(3).unwrap().parse::<u32>().unwrap();
            assert!(number == counter);
            map.insert(*current_year.as_ref().unwrap(), number);
            current_year = None;
        } else {
            counter = counter + 1;
        }
    }
    return map;
}
