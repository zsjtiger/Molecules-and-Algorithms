-- LaTeX-only transforms: SVG→PDF figure paths, custom divs → tcolorbox
if not FORMAT:match("latex") then return {} end

-- 1) images/svg/foo.svg  ->  images/png/foo.pdf  (figkit writes PDFs there)
function Image(el)
  local p = el.src:gsub("images/svg/([^/]+)%.svg$", "images/png/%1.pdf")
  el.src = p
  return el
end

-- 2) custom divs that only had SCSS styling in HTML
function Div(el)
  if el.classes:includes("fallacy-pitfall") then
    return {
      pandoc.RawBlock("latex", "\\begin{fpbox}"),
      pandoc.Div(el.content),
      pandoc.RawBlock("latex", "\\end{fpbox}")
    }
  end
  if el.classes:includes("purpose-question") then
    return {
      pandoc.RawBlock("latex", "\\begin{purposebox}"),
      pandoc.Div(el.content),
      pandoc.RawBlock("latex", "\\end{purposebox}")
    }
  end
end
