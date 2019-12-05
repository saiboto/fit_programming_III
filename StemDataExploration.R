install.packages('pastecs')
library(pastecs)


setwd('C:\\Users\\tmi640\\Desktop')
d <- read.csv('Brandenburg_Aufnahme10.2019.csv', sep = ";", dec = ",")

attach(d)

# Durchmesserverteilung ------------
hist(D1..Stirn)
stat.desc(D1..Stirn)
hist(D2.Stirn)
stat.desc(D2.Stirn)
hist(D1.Mitte)
stat.desc(D1.Mitte)
hist(D2.Mitte)
stat.desc(D2.Mitte)
hist(D1.Zopf)
stat.desc(D1.Zopf)
hist(D2.Zopf)
stat.desc(D2.Zopf)

# Abholzigkeit --------------------
plot(D1..Stirn , D1.Zopf)
lines(x = c(0,100), y = c(0,100))
stat.desc(D1..Stirn/D1.Zopf)
hist(D1..Stirn/D1.Zopf)
stat.desc(D1..Stirn-D1.Zopf)
hist(D1..Stirn-D1.Zopf)

plot(D2.Stirn , D2.Zopf)
lines(x = c(0,100), y = c(0,100))
hist(D2.Stirn/D2.Zopf)
stat.desc(D2.Stirn/D2.Zopf)
hist(D2.Stirn-D2.Zopf)
stat.desc(D2.Stirn-D2.Zopf)

a <- D1..Stirn/D1.Zopf
b <- D1..Stirn-D1.Zopf
plot(D1..Stirn ~ a)
plot(D1..Stirn ~ b)
lm(D1..Stirn ~ a)
lm(D1..Stirn ~ b)

# Elliptik --------------------------
plot(D1..Stirn ~ D2.Stirn) + lines(x = c(0,100), y = c(0,100))
plot(D1.Mitte ~ D2.Mitte) + lines(x = c(0,100), y = c(0,100))
plot(D1.Zopf ~ D2.Zopf) + lines(x = c(0,100), y = c(0,100))
hist(D1..Stirn/D2.Stirn)
hist(D1.Mitte/D2.Mitte)
hist(D1.Zopf/D2.Zopf)

# Krümmung -----------------------
# Einheit ist mm, über die ganze Länge des Stamms
hist(Krümmung.h, breaks = 20)

plot(Krümmung.h ~ D1..Stirn)
lm(Krümmung.h ~ D1..Stirn)

# Sonstiges ------------------------
hist(Länge, breaks = 20)
stat.desc(Länge)

hist(Rindenstärke)
plot(Rindenstärke ~ D2.Stirn)
