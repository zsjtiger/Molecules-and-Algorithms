-- Map MLSysBook-style custom callouts to Quarto callouts with Chinese default titles.
local map = {
  ["callout-learning-objectives"] = {"tip",       "学习目标",   "lo"},
  ["callout-definition"]          = {"note",      "定义",       "def"},
  ["callout-example"]             = {"note",      "示例",       "ex"},
  ["callout-war-story"]           = {"warning",   "案例与教训", "ws"},
  ["callout-checkpoint"]          = {"tip",       "自测检查点", "chk"},
  ["callout-perspective"]         = {"note",      "视角",       "persp"},
  ["callout-principle"]           = {"important", "原则",       "pri"},
  ["callout-takeaways"]           = {"important", "本章要点",   "tk"},
  ["callout-chapter-connection"]  = {"note",      "下一章",     "cc"},
  ["callout-lighthouse"]          = {"note",      "标杆案例",   "lh"},
}
function Div(el)
  for cls, spec in pairs(map) do
    if el.classes:includes(cls) then
      local newclasses = pandoc.List({"callout-" .. spec[1], "cb-" .. spec[3]})
      for _, c in ipairs(el.classes) do
        if c ~= cls then newclasses:insert(c) end
      end
      el.classes = newclasses
      local t = el.attributes["title"]
      local numbered = el.identifier ~= nil and el.identifier ~= ""
      if t == nil or t == "" then
        -- numbered callouts get "定义 1.2" etc. from Quarto; a generic
        -- default title would render as "检查点 1.1：自测检查点"
        if not numbered then el.attributes["title"] = spec[2] end
      elseif not numbered then
        el.attributes["title"] = spec[2] .. "：" .. t
      end
      if spec[3] == "tk" or spec[3] == "lo" or spec[3] == "chk" then
        el.attributes["collapse"] = el.attributes["collapse"] or nil
      end
      return el
    end
  end
  if el.classes:includes("fallacy-pitfall") then
    el.classes:insert("fp-box")
    return el
  end
end

-- Map MLSysBook id prefixes to Quarto cross-referenceable callout prefixes.
local idmap = { ["dfn-"]="nte-", ["pri-"]="imp-", ["ws-"]="wrn-", ["chk-"]="tip-", ["lh-"]="cau-" }
local function remap(id)
  for a, b in pairs(idmap) do
    if id:sub(1, #a) == a then return b .. id:sub(#a + 1) end
  end
  return nil
end
local _Div = Div
function Div(el)
  local r = _Div(el) or el
  if r.identifier and r.identifier ~= "" then
    local n = remap(r.identifier); if n then r.identifier = n end
  end
  return r
end
function Cite(el)
  for _, c in ipairs(el.citations) do
    local n = remap(c.id); if n then c.id = n end
  end
  return el
end
