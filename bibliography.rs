#!/usr/bin/env rust-script
//! ```cargo
//! [dependencies]
//! mdbook = "0.4.4"
//! clap = "2.33.3"
//! pandoc = "0.8.1"
//! serde = "1.0.118"
//! serde_json = "1.0.61"
//! ```
use clap::{App, Arg, SubCommand};
use mdbook::book::{Book, BookItem};
use mdbook::errors::Error;
use mdbook::preprocess::{CmdPreprocessor, Preprocessor, PreprocessorContext};
use std::io;
use std::process;
use pandoc::PandocOutput::ToBuffer;
use std::path::{Path, PathBuf};

fn main() {
    let app = App::new("bibliography.rs")
        .arg(Arg::with_name("bib")
            .required(true)
            .takes_value(true))
        .arg(Arg::with_name("csl")
            .required(true)
            .takes_value(true))
        .subcommand(
            SubCommand::with_name("supports")
                .arg(Arg::with_name("renderer").required(true))
                .about("Check whether a renderer is supported by this preprocessor"),
        );
    let matches = app.get_matches();

    if let Some(_) = matches.subcommand_matches("supports") {
        process::exit(0);
    }

    let bib = Path::new(matches.value_of("bib").unwrap());
    let csl = Path::new(matches.value_of("csl").unwrap());
    let preprocessor = Bibliography::new(bib, csl);
    if let Err(e) = handle_preprocessing(&preprocessor) {
        eprintln!("{}", e);
        process::exit(1);
    }
}

fn handle_preprocessing(pre: &dyn Preprocessor) -> Result<(), Error> {
    let (ctx, book) = CmdPreprocessor::parse_input(io::stdin())?;

    if ctx.mdbook_version != mdbook::MDBOOK_VERSION {
        eprintln!(
            "Warning: The {} plugin was built against version {} of mdbook, \
             but we're being called from version {}",
            pre.name(),
            mdbook::MDBOOK_VERSION,
            ctx.mdbook_version
        );
    }
    let processed_book = pre.run(&ctx, book)?;
    serde_json::to_writer(io::stdout(), &processed_book)?;
    Ok(())
}

pub struct Bibliography {
    bib: PathBuf,
    csl: PathBuf,
}

impl Bibliography {

    pub fn new(bib: &Path, csl: &Path) -> Self {
        if !bib.exists() {
            panic!("Bib file not found");
        }
        if !csl.exists() {
            panic!("CSL file not found");
        }
        Bibliography {
            bib: bib.to_owned(),
            csl: csl.to_owned()
        }
    }

}

impl Preprocessor for Bibliography {
    fn name(&self) -> &str {
        "pandoc-bibliography"
    }

    fn run(&self, _ctx: &PreprocessorContext, mut book: Book) -> Result<Book, Error> {
        book.for_each_mut(|item| {
            if let BookItem::Chapter(chapter) = item {
                let mut p = pandoc::new();
                p.set_input(pandoc::InputKind::Pipe(chapter.content.clone()));
                p.add_option(pandoc::PandocOption::Filter("pandoc-citeproc".into()));
                p.add_option(pandoc::PandocOption::Csl(self.csl.clone()));
                p.set_bibliography(&self.bib);
                p.set_output(pandoc::OutputKind::Pipe);
                p.set_output_format(pandoc::OutputFormat::MarkdownStrict, vec![]);
                if let ToBuffer(x) = p.execute().unwrap() {
                    chapter.content = x;
                }
            }
        });
        Ok(book)
    }
}
