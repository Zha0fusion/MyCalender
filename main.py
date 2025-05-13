from datetime import datetime
from zhdate import ZhDate
import requests
from icalendar import Calendar
from datetime import datetime, date, timedelta
from dateutil.rrule import rrulestr
import pytz
from bs4 import BeautifulSoup

#声明变量
chinesedate = "二零二五年四月初九 乙巳年 (蛇年)"
day = 6
fulldate = "2025年5月6日 星期三"

num_week = 6
percentage = "67%"

schedule = "测试\n测试\n测试"
url = "https://p215-caldav.icloud.com.cn/published/2/MTY5NDM3NDIyODkxNjk0MxQGglZSrjcCCgbEAcXHCbH1PEeMJlXixNdWItQaJ3vTpLQG9mBKbwfAoA3nGulbAnNxSzx-Nh8QY1dQ9ZSBoTQ"
disp_time = datetime.now().strftime("%H:%M")

#实现代码
#---------------农历str------------
def getChineseDate():
    today = ZhDate.today()
    chinesedate = today.chinese()
    return chinesedate
    
#------------日程表----------------
def getSchedule():
    import requests
    from icalendar import Calendar
    from datetime import datetime, date, timedelta
    from dateutil.rrule import rrulestr

    url = "https://p215-caldav.icloud.com.cn/published/2/MTY5NDM3NDIyODkxNjk0MxQGglZSrjcCCgbEAcXHCbH1PEeMJlXixNdWItQaJ3vTpLQG9mBKbwfAoA3nGulbAnNxSzx-Nh8QY1dQ9ZSBoTQ"
    response = requests.get(url)
    if response.status_code != 200:
        return "（日程加载失败）"

    cal = Calendar.from_ical(response.text)
    today = date.today()

    all_day_events = []
    timed_events = []

    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        summary = component.get("summary")
        description = component.get("description")
        dtstart = component.get("dtstart").dt
        dtend = component.get("dtend").dt

        # 判断是否是全天事件
        if isinstance(dtstart, date) and not isinstance(dtstart, datetime):
            if dtstart == today:
                all_day_events.append({
                    "title": summary,
                    "desc": description
                })
        else:
            # 时间事件处理
            tzinfo = dtstart.tzinfo
            start_of_today = datetime.combine(today, datetime.min.time()).replace(tzinfo=tzinfo)
            end_of_today = datetime.combine(today + timedelta(days=1), datetime.min.time()).replace(tzinfo=tzinfo)


            if component.get('rrule'):
                rule_str = component.get('rrule').to_ical().decode()
                rule = rrulestr(rule_str, dtstart=dtstart)
                occurrences = rule.between(start_of_today, end_of_today, inc=True)

                for occur in occurrences:
                    timed_events.append({
                        "title": summary,
                        "start": occur,
                        "end": occur + (dtend - dtstart),
                        "desc": description
                    })
            else:
                if dtstart.date() == today:
                    timed_events.append({
                        "title": summary,
                        "start": dtstart,
                        "end": dtend,
                        "desc": description
                    })

    # 构建输出字符串
    output_lines = []

    for event in all_day_events:
        output_lines.append(f" ·{event['title']} 全天")
        if event["desc"]:
            output_lines.append(f" （{event['desc']}）")

    if timed_events:
        timed_events.sort(key=lambda e: e["start"])
        for event in timed_events:
            start_time = event["start"].strftime("%H:%M")
            end_time = event["end"].strftime("%H:%M")
            output_lines.append(f" ·{event['title']} {start_time}-{end_time}")
            if event["desc"]:
                output_lines.append(f" （{event['desc']}）")

    if not all_day_events and not timed_events:
        output_lines.append(f"今天（{today}）没有事件。")

    return "\n".join(output_lines)

#-----------获取天数---------------
def getDay():
    today = date.today()
    day = today.day
    return day
    
#-----------获取完整日期-----------
def getFulldate():
    today = date(2025, 5, 6)  # 你也可以用 date.today()
    weekday_cn = "星期" + "一二三四五六日"[today.weekday()]
    fulldate = f"{today.year}年{today.month}月{today.day}日 {weekday_cn}"
    return fulldate
#-----------获取学期周-------------
def getWeek():
    semester_start = date(2025, 3, 28)

    # 今天日期（你也可以手动指定）
    today = date.today()

    # 计算周数（+1 表示第几周，从1开始）
    delta_days = (today - semester_start).days
    week_number = delta_days // 7 + 1
    return week_number

#---------获取当前时间降水概率-------
def getPercentage():
    url = "https://weather.com/zh-CN/weather/hourbyhour/l/Kuala%2BLumpur%2BMalaysia?canonicalCityId=91a6f9c5c0d51f40d6a3eb94a0498ed0"
    headers = {
    "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 只获取第一个降水概率
    first_precip = soup.find('span', attrs={"data-testid": "PercentageValue"})

    if first_precip:
        return first_precip.get_text()
    else:
        return"未找到"

#----------统一部署自定义函数--------
chinesedate = getChineseDate()

schedule = getSchedule()

day = getDay()

fulldate = getFulldate()

num_week = getWeek()

week = "Week " + str(num_week)

percentage = getPercentage()

print(day)

#----------添加到html-------------

with open("panel.html", "r", encoding="utf-8") as f:
    panel = f.read()

html = panel.replace("{{chinesedate}}", chinesedate)\
               .replace("{{date}}", str(day))\
               .replace("{{fulldate}}",fulldate)\
               .replace("{{week}}", week)\
               .replace("{{percentage}}", percentage)\
               .replace("{{schedule}}", schedule)\
               .replace("{{time}}", disp_time) 

with open("calendar.html", "w", encoding="utf-8") as f:
    f.write(html)