// Minimal IEEE conference layout for Typst, self-contained (no package download).
// API mirrors @preview/charged-ieee so paper.typ can switch to that package later:
//   #import "@preview/charged-ieee:0.1.3": ieee
// US Letter, two columns, Times 10pt, IEEE heading and caption styles.

#let ieee(
  title: [],
  abstract: none,
  authors: (),
  index-terms: (),
  bibliography: none,
  body,
) = {
  set document(title: title, author: authors.map(a => a.name))
  set page(
    paper: "us-letter",
    margin: (top: 0.75in, bottom: 1in, x: 0.625in),
    columns: 2,
  )
  set columns(gutter: 0.2in)
  set text(font: ("Times New Roman", "Liberation Serif", "TeX Gyre Termes", "Nimbus Roman"), size: 10pt)
  set par(justify: true, first-line-indent: 1em, leading: 0.5em, spacing: 0.5em)

  // Headings: IEEE style — I. SMALL CAPS centred; A. Italic; 1) italic run-in.
  set heading(numbering: "I.A.1)")
  show heading: it => {
    set text(size: 10pt, weight: "regular")
    if it.level == 1 {
      set align(center)
      set text(size: 10pt)
      block(above: 1.4em, below: 0.9em)[
        #numbering("I.", counter(heading).get().first())
        #h(0.4em)
        #smallcaps(it.body)
      ]
    } else if it.level == 2 {
      block(above: 1.2em, below: 0.7em)[
        #emph[#numbering("A.", counter(heading).get().last())#h(0.4em)#it.body]
      ]
    } else {
      box(inset: (right: 0.4em))[#emph[#numbering("1)", counter(heading).get().last())#h(0.3em)#it.body:]]
    }
  }

  // Figures and tables
  show figure.caption: it => {
    set text(size: 8pt)
    set align(center)
    it
  }
  show figure.where(kind: table): set figure.caption(position: top)
  show figure.where(kind: table): it => {
    set text(size: 8pt)
    show figure.caption: c => [#smallcaps[TABLE #c.counter.display(c.numbering)] \ #smallcaps(c.body)]
    it
  }
  show figure.where(kind: image): it => {
    show figure.caption: c => [Fig. #c.counter.display(c.numbering). #c.body]
    it
  }
  set table(stroke: (x, y) => if y == 0 { (bottom: 0.5pt, top: 0.5pt) } else { none }, inset: 4pt)
  show table: set text(size: 8pt)

  // Code
  show raw.where(block: true): set text(size: 8pt)
  show raw.where(block: true): block.with(inset: (x: 0pt, y: 4pt))

  // Links
  show link: set text(fill: rgb("#1a3d7c"))

  // Title block spans both columns
  place(top, float: true, scope: "parent", clearance: 1.5em)[
    #set align(center)
    #set par(first-line-indent: 0em)
    #text(size: 24pt, weight: "regular")[#title]
    #v(0.6em)
    #let cols = calc.min(authors.len(), 4)
    #grid(
      columns: (1fr,) * cols,
      row-gutter: 1.2em,
      column-gutter: 1em,
      ..authors.map(a => [
        #set text(size: 10pt)
        #a.name \
        #set text(size: 9pt)
        #if "department" in a [#emph(a.department) \ ]
        #if "organization" in a [#emph(a.organization) \ ]
        #if "location" in a [#a.location \ ]
        #if "email" in a [#raw(a.email)]
      ])
    )
    #v(0.4em)
  ]

  // Abstract and index terms
  set par(first-line-indent: 0em)
  if abstract != none [
    #set text(size: 9pt, weight: "bold")
    #emph[Abstract]---#abstract
    #v(0.5em)
  ]
  if index-terms.len() > 0 [
    #set text(size: 9pt, weight: "bold")
    #emph[Index Terms]---#index-terms.join(", ")
    #v(0.8em)
  ]
  set par(first-line-indent: 1em)

  body

  if bibliography != none {
    set text(size: 8pt)
    show heading: set text(size: 10pt)
    bibliography
  }
}
