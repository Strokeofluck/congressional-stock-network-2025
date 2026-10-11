# Maintenance helper: create bounded House references from exact upstream YAML.
# The analysis reads the resulting versioned files; this helper is not run on render.
# Supply source-cache/<commit>/<filename> from the URLs in data/2025/source-manifest.json.
library(yaml)
library(jsonlite)
index <- read.csv('committee-snapshot-index-2025.csv', stringsAsFactors=FALSE)
roster_commit <- '82b1eaccd2cad9e4172059507f5129fc513962af'
source_paths <- character()
for (commit in index$source_commit) {
  metadata <- yaml::read_yaml(file.path('source-cache',commit,'committees-current.yaml'))
  house_ids <- vapply(Filter(function(entry) identical(entry$type,'house'),metadata),function(entry) entry$thomas_id,character(1))
  for (name in c('committee-membership-current.yaml','committees-current.yaml')) {
    input <- file.path('source-cache',commit,name)
    x <- yaml::read_yaml(input)
    if (name == 'committee-membership-current.yaml') {
      # House Intelligence uses HLIG; parent type is authoritative, not HS prefix.
      x <- x[vapply(names(x),function(key) any(startsWith(key,house_ids)),logical(1))]
    } else {
      x <- Filter(function(entry) identical(entry$type,'house'),x)
    }
    output <- file.path('data/2025/reference',commit,name)
    dir.create(dirname(output),recursive=TRUE,showWarnings=FALSE)
    yaml::write_yaml(x,output)
    source_paths <- c(source_paths,paste0(commit,'/',name))
  }
}
for (name in c('legislators-current.yaml','legislators-historical.yaml')) {
  x <- yaml::read_yaml(file.path('source-cache',roster_commit,name))
  x <- lapply(x,function(person){
    terms <- Filter(function(term) identical(term$type,'rep') &&
      as.character(term$start) <= '2025-12-31' && as.character(term$end) > '2025-01-03',person$terms)
    if (!length(terms)) return(NULL)
    list(id=list(bioguide=person$id$bioguide),name=person$name,terms=terms)
  })
  x <- Filter(Negate(is.null),x)
  output <- file.path('data/2025/reference',roster_commit,name)
  dir.create(dirname(output),recursive=TRUE,showWarnings=FALSE)
  yaml::write_yaml(x,output)
  source_paths <- c(source_paths,paste0(roster_commit,'/',name))
}
dir.create('build',showWarnings=FALSE)
write_json(source_paths,'build/reference-paths.json',pretty=TRUE,auto_unbox=TRUE)
