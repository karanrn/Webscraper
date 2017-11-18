'''
Author: Karan R Nadagoudar
Date: 18/11/2017
Descripition: Extract market price of commodity from agmarknet.nic.in
'''

# Using Beautiful soup for extrating html content
# Splinter for navigating the website
def extract_info(year,month,state,commodity):
    import bs4
    from splinter import Browser
    bw = Browser()
    bw = Browser(headless=True)
    url = 'http://www.agmarknet.nic.in/agnew/NationalBEnglish/DatewiseCommodityReport.aspx'
    bw.visit(url)

    # Information for querying 
    Year = year
    month = month
    commodity = commodity
    state = state
    bw.select('cboYear',Year)
    bw.select('cboMonth',month)
    bw.select('cboState',state)
    bw.select_by_text('cboCommodity',commodity)
    # submitting the inputs to server
    bw.find_by_name('btnSubmit').click()

    # Extracting information from html
    page = bs4.BeautifulSoup(bw.html,'html.parser')
    tables = page.find_all('table',id='gridRecords')
    headers = []
    values = []
    for i in page.find_all('table', id='gridRecords'):
        for t in i.find_all('tbody'):
            for r in t.find_all('th'):
                headers.append(r.text)
            count = 0
            for r2 in t.find_all('tr'):
                xx=[]
                for r3 in r2.find_all('td'):
                    xx.append(r3.text)
                values.append(xx)
    values.pop(0)

    # Converting extracted data to dataframe
    import pandas as pd
    df = pd.DataFrame(values,columns=headers)
    df.to_csv('market_prices.csv',sep=',')

def main():
    print("Enter the details below to get market prices:\n")
    year = input("Enter the year:")
    month = input("Enter the month (ex:November):")
    state = input("Enter the state name (ex:Karnataka):")
    commodity = input("Enter the commodity:")
    extract_info(year,month,state,commodity)

if __name__ == '__main__':
    main()