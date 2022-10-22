### Importing modules
import json
import urllib
import urllib.request
import urllib.error
import urllib.parse
import os

### Function that does an http get to download the list of apps that returned in JSON format


def get_apps(limit, offset, filter=''):

  ### Base URL to download list of apps
  base_url = "https://splunkbase.splunk.com/api/v1/app/?order=latest&limit=" + \
      str(limit) + "&include=support,created_by,categories,icon,screenshots,rating,releases,documentation,releases.content,releases.splunk_compatibility,releases.cim_compatibility,releases.install_method_single,releases.install_method_distributed,release,release.content,release.cim_compatibility,release.install_method_single,release.install_method_distributed,release.splunk_compatibility" + "&offset="

  ### Build the url to download the list of apps
  url = base_url + str(offset) + "&" + filter

  ### This takes a python object and dumps it to a string which is a JSON representation of that object
  data = json.load(urllib.request.urlopen(url))

  ### Return the json data
  return data

### Iterate through the list of apps and print the json format


def print_json(apps):
  app_text = ''
  for app in list(apps):
    jsonText = json.dumps(app, indent=2)
    app_text += jsonText + "\n"
  return app_text

### Convert the json to a csv for a given set specified fields


def to_csv(apps, product_category='enterprise', headers=['uid', 'title']):
  csv_row = ''
  for app in apps:
    csv_str = ''
    ### Convert it to a csv text
    for field in headers:
      field = str(app[field])
      csv_str += field + ","
    ### Remove the last comma
    csv_row += product_category + "," + csv_str.rstrip(',') + "\n"
  return csv_row


def iterate_apps(app_func, app_filter=''):
  offset = 0
  limit = 100
  counter = 0
  total = 1

  while counter < total:
    # Download initial list of the apps
    data = get_apps(limit, offset, app_filter)
    total = data['total']  # Get the total number of apps
    apps = data['results']  # Get the results

    yield app_func(apps)
    offset += limit
    counter = counter + 100


def main():
  def app_func(x): return print_json(x)
  for app_json in iterate_apps(app_func):
    print(app_json)


if __name__ == "__main__":
  main()
