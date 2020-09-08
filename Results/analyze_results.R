setwd("/home/timon/fit_programming_III")

d <- read.csv("Resulting_Measurements.csv")

s <- read.csv("My_Stems.csv")

hist(s$middle_diam_x)

hist(d$Deflation.Factor)

hist(d$Front.Area)
