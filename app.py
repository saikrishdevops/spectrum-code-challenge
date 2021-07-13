from flask import Flask,request,Response
import os
import requests
from flask import jsonify
import pandas as pd



app = Flask(__name__)

url = "https://www.energy.gov/sites/prod/files/2020/12/f81/code-12-15-2020.json"

@app.route("/")
def hello():
    return "Flask inside Docker!!"


# {
#  "organizations": [
#  {
#  "organization": "Generic Organization Name",
#  "release_count": 20,
#  "total_labor_hours": 4894,
#  "all_in_production": false,
#  "licenses": ["LGPL-2.1"],
#  "most_active_months": [5],
#  },
#  ...
#  ]
# }


@app.route("/json")
def json_data():
    
    sortby = request.args.get('sort')

    print("=======sort",sortby)

    resp = requests.get(url=url)
    data = resp.json()
    organizations_list = []
    #updated_data = data["releases"][0]

    #orgsset = set()

    orgsset = set([eachorg["organization"] for eachorg in data["releases"]])


    for org in orgsset:

        tempdict = {}
        each_org_data = [eachorg for eachorg in data["releases"] if eachorg["organization"] == org]
        tempdict["organization"] = org
        tempdict["release_count"] = len(each_org_data)

        laborHours = 0
        allrelease_flag = True
        licenses_list = set()
        arrayOfmonth = set()
        for each in each_org_data:

            laborHours = laborHours + each["laborHours"]

            arrayOfmonth.add(each["date"]["created"])

            for eachlice in each["permissions"]["licenses"]:
                licenses_list.add(eachlice["name"])             

            allrelease_flag_list = []
            if len(allrelease_flag_list) == 0 and each["status"] != 'Production':
                allrelease_flag = False
                allrelease_flag_list.append(False)
            

        tempdict["total_labor_hours"] = round(laborHours)
        tempdict["all_in_production"] = allrelease_flag
        tempdict["licenses"] = list(licenses_list)
        tempdict["most_active_months"] = len(list(arrayOfmonth))


        organizations_list.append(tempdict)

    if sortby and sortby in tempdict.keys():
        organizations_list = sorted(organizations_list, key=lambda k: k[sortby]) 


    
    return jsonify(organizations_list)


@app.route("/csv")
def csv_data():
    
    sortby = request.args.get('sort')

    print("=======sort",sortby)

    resp = requests.get(url=url)
    data = resp.json()
    organizations_list = []
    #updated_data = data["releases"][0]

    #orgsset = set()

    orgsset = set([eachorg["organization"] for eachorg in data["releases"]])


    for org in orgsset:

        tempdict = {}
        each_org_data = [eachorg for eachorg in data["releases"] if eachorg["organization"] == org]
        tempdict["organization"] = org
        tempdict["release_count"] = len(each_org_data)

        laborHours = 0
        allrelease_flag = True
        licenses_list = set()
        arrayOfmonth = set()
        for each in each_org_data:

            laborHours = laborHours + each["laborHours"]

            arrayOfmonth.add(each["date"]["created"])

            for eachlice in each["permissions"]["licenses"]:
                licenses_list.add(eachlice["name"])             

            allrelease_flag_list = []
            if len(allrelease_flag_list) == 0 and each["status"] != 'Production':
                allrelease_flag = False
                allrelease_flag_list.append(False)
            

        tempdict["total_labor_hours"] = round(laborHours)
        tempdict["all_in_production"] = allrelease_flag
        tempdict["licenses"] = list(licenses_list)
        tempdict["most_active_months"] = len(list(arrayOfmonth))


        organizations_list.append(tempdict)

    if sortby and sortby in tempdict.keys():
        organizations_list = sorted(organizations_list, key=lambda k: k[sortby]) 

        
    df = pd.DataFrame(organizations_list)

    return Response(
        df.to_csv(),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=orgs_data.csv"})



@app.route("/getPlotCSV")
def getPlotCSV():
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    csv = '1,2,3\n4,5,6\n'

    data = {'name': ['nick', 'david', 'joe', 'ross'],'age': ['5', '10', '7', '6']} 
    df = pd.DataFrame.from_dict(data)
    return Response(
        df.to_csv(),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
