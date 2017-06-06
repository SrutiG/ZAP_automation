import ZAPCommon

def concatenateReports(jsonLst):
	alerts = []
	for alertLst in jsonLst:
		alerts += alertLst
	return alerts

def orderedAlerts(alerts):
	formattedAlerts = {}
	for alert in alerts:
		if not alert["name"] in list(formattedAlerts):
			formattedAlerts[alert["name"]] = {"description":alert["description"], "solution": alert["solution"], "risk": alert["risk"], "confidence": alert["confidence"], "urls": [alert["url"]]}
		else:
			formattedAlerts[alert["name"]]["urls"].append(alert["url"])
	orderedAlerts = []
	for alert, descript in formattedAlerts.iteritems():
		orderedAlerts.append((alert, descript))
	orderedAlerts = sorted(orderedAlerts, key = lambda x : priority(x[1]["risk"]))
	return orderedAlerts

def priority(risk):
	if risk == "High":
		return 1
	elif risk == "Medium":
		return 2
	elif risk == "Low":
		return 3
	elif risk == "Information":
		return 4
	else:
		return 5

def getRisk(alerts):
	risk = {"High":0, "Medium":0, "Low":0, "Information":0}
	for alert in alerts:
		risk[alert["risk"]] += 1
	return risk

def getColors():
	return {"High":{"text":"text-danger", "bg":"bg-danger"}, "Medium":{"text":"text-warning", "bg":"bg-warning"}, "Low":{"text":"text-success", "bg":"bg-success"}, "High":{"text":"text-info", "bg":"bg-info"}}

def createHTMLReport(alerts):
	orderedAlerts = orderedAlerts(alerts)
	risk = getRisk(alerts)
	colors = getColors()
	htmlReport = open("htmlReport.html", "w")
	htmlReport.write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>HTML Report</title><style>:root {--low: #333;--main-bgrd: #FFF;--alert: #CCC;}body {background-color: var(--main-bgrd) ! important;width: 100vw;}details summary::-webkit-details-marker { display:none; }summary{outline:none;display:block;}ul summary{display:block;list-style:none;}.main {background-color: inherit ! important;padding: 0 ! important;}.alert{background-color: var(--main-bgrd);padding: 2% ! important;border-bottom: 1px solid var(--alert) ! important;}.risk-table {width: 30% ! important;margin: 2%' + ' auto;}.risk-item {width: 150px;padding: 0.75%;margin-top: 10%;color: #444;}.risk-item:hover {text-decoration: none ! important;}</style><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"><script type="text/javascript" src="report.js"></script></head>')
	htmlReport.write('<body><ul class="list-inline text-center"><li><div class="bg-danger risk-item"><h3 class="text-uppercase lead">high<br>%d</h3></div></li>'%risk["High"])
	htmlReport.write('<li><div class="bg-warning risk-item"><h3 class="text-uppercase lead">medium<br>%d</h3></div></li>'%risk["Medium"])
	htmlReport.write('<li><div class="bg-success risk-item"><h3 class="text-uppercase lead">low<br>%d</h3></div></li>'%risk["Low"])
	htmlReport.write('<li><div class="bg-info risk-item"><h3 class="text-uppercase lead">info<br>%d</h3></div></li>'%risk["Information"])
	htmlReport.write('</ul>')
	htmlReport.write('<div class="jumbotron main"><div class="alerts"><ul class="container">')

	for alert in orderedAlerts:
		risk = alert[1]["risk"]
		confidence = alert[1]["confidence"]
		htmlReport.write('<li class="alert list-unstyled">')
		htmlReport.write('<details>')

		htmlReport.write('<summary><h2><strong>%s (%d) </strong><span class="%s">* </span><span class="caret"></span></h2></summary>'%(alert[0], len(alert[1]["urls"]),colors[risk]["text"]))
		htmlReport.write('<div><br>')
		htmlReport.write('<h3>Risk: <strong><span class="%s">%s</span></strong></h3>'%(colors[risk]["text"], risk))
		htmlReport.write('<br>')
		htmlReport.write('<h3>Confidence: <strong><span class="%s">%s</span></strong></h3>'%(colors[confidence]["text"], confidence))
		htmlReport.write('<br>')
		htmlReport.write('<h3>Description: <br><small>%s</small></h3>'%alert[1]["description"])
		htmlReport.write('<br>')
		htmlReport.write('<h3>Solution: <br><small>%s</small></h3>'%alert[1]["solution"])
		htmlReport.write('<br>')
		htmlReport.write('<h3>URLs: </h3><ul class="list-unstyled">')
		if (len(alert[1]["urls"]) <= 5):
			for url in alert[1]["urls"]:
				htmlReport.write('<li><h4><small>%s</small></h4></li>'%url)
		else:
			htmlReport.write('<details>')
			htmlReport.write('<summary>')
			htmlReport.write('<li><h4><small>%s</small></h4></li>'%alert[1]["urls"][0])
			htmlReport.write('<li><h4><small>%s</small></h4></li>'%alert[1]["urls"][1])
			htmlReport.write('<li><h4><small>%s</small></h4></li>'%alert[1]["urls"][2])
			htmlReport.write('<li><h4><small>%s</small></h4></li>'%alert[1]["urls"][3])
			htmlReport.write('<li><h4><small>%s</small></h4></li>'%alert[1]["urls"][4])
			htmlReport.write('<li><a><h4><small>More...</small></h4></a></li>')
			htmlReport.write('</summary>')
			for x in range(5,len(alert[1]["urls"])):
				htmlReport.write('<li><h4><small>%s</small></h4></li>'%url)
			htmlReport.write('</details>')

		htmlReport.write('</ul>')
		#htmlReport.write('<br>')
		#htmlReport.write('<a href="https://www.owasp.org/index.php/HttpOnly" target="_blank"><h4><b>More Info</b></h4></a>')
		htmlReport.write('</div>')
		htmlReport.write('</details>')
		htmlReport.write('</li>')

	htmlReport.write('</ul></div></div></body></html>')

if __name__ == "__main__":
	ZAP_Common = ZAPCommon.ZAPCommon()
	alerts = ZAP_Common.getScanAlerts()['alerts']
	createHTMLReport(alerts)

