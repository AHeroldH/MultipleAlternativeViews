# R by default creates a warning when loading a library (even when successful)
# we suppress this message here -- in the case the loading fails we try to
# reload but this time with warnings enabled to get a proper error message
if(!suppressMessages(require(scagnostics))) {
  require(scagnostics)
}

scags <- function(x=(0:4919), y=(0:4919)) {
  return(binostics::scagnostics(x, y))
}

