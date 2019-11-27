const execSync = require('child_process').execSync
const fs = require('fs') 

const getPid = (process_name) => {
	try {
		cmd2 = "adb shell ps | grep " + process_name
		return execSync(cmd2).toString('utf-8').split(" ").filter((x) => x !== "")[1]
	} catch (e) {
		return '9999'
	}
}

const lmkd = getPid('lmkd')
const kswapd = getPid('kswapd')
const medias = getPid('medias')
const surface = getPid('surface')

const process_name = 'firefox:media'
let media_pid = getPid(process_name)

const process_name2 = 'mozilla.firefox'
let firefox_pid = getPid(process_name2)

/*setInterval(() => {
	try {
		let cmd1 = "adb shell dumpsys meminfo " + firefox_pid + " | grep TOTAL"
		let stdout = execSync(cmd1).toString('utf-8')
		stdout += execSync("adb shell echo \\$EPOCHREALTIME").toString('utf-8')
		fs.appendFile('pss_firefox_data.txt', stdout, (err) => {if (err) throw err;})
	} catch (err) {
		try {
			cmd2 = "adb shell ps -A | grep " + process_name2
			firefox_pid = execSync(cmd2).toString('utf-8').split(" ").filter((x) => x !== "")[1]
			console.log(firefox_pid)
		} catch (e) {}
	}
}, 500)*/

setInterval(() => {
	// try {
		let cmd1 = "adb shell 'cat /proc/stat; cat /proc/" + lmkd + "/stat; \
		cat /proc/" + kswapd + "/stat; cat /proc/" + medias + "/stat; cat /proc/" + surface + "/stat; \
		cat /proc/" + firefox_pid + "/stat; cat /proc/" + media_pid + "/stat; \
		echo \$EPOCHREALTIME;'"
		let stdout = execSync(cmd1).toString('utf-8')
		if (stdout.includes("No such file or directory")) {
			try {
			cmd2 = "adb shell ps | grep " + process_name
			media_pid = execSync(cmd2).toString('utf-8').split(" ").filter((x) => x !== "")[1]
			cmd2 = "adb shell ps | grep " + process_name2
			firefox_pid = execSync(cmd2).toString('utf-8').split(" ").filter((x) => x !== "")[1]
			} catch (e) {}
		}
		fs.appendFile('cpu_data.txt', stdout, (err) => {if (err) throw err;})
	// }
	// catch (err) {
	// 	try {
	// 		cmd2 = "adb shell ps -A | grep " + process_name
	// 		media_pid = execSync(cmd2).toString('utf-8').split(" ").filter((x) => x !== "")[1]
	// 		cmd2 = "adb shell ps -A | grep " + process_name2
	// 		firefox_pid = execSync(cmd2).toString('utf-8').split(" ").filter((x) => x !== "")[1]
	// 	} catch (e) {}
	// }
}, 500)

setInterval(() => {
	let cmd = "adb shell 'cat /proc/meminfo; echo \$EPOCHREALTIME;'"
	let stdout = execSync(cmd).toString('utf-8')
	fs.appendFile('mem_data.txt', stdout, (err) => {if (err) throw err;})
}, 500)

setInterval(() => {
	let cmd = "adb shell 'cat /proc/vmstat; echo \$EPOCHREALTIME;'"
	let stdout = execSync(cmd).toString('utf-8')
	fs.appendFile('vmstat_data.txt', stdout, (err) => {if (err) throw err;})
}, 500)
