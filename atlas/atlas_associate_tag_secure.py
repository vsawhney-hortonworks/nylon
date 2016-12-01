#!/usr/bin/python
import argparse
import requests
import json
import sys
import string
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
from requests.packages.urllib3.exceptions import InsecureRequestWarning
###################################################################################
### Usage: For tagging Table:
###   python atlas_associate_tag.py --atlas_server_uri atlas.server.fqdn:port \
###    --atlas_table_FQDN default.students_compute:qrs@turing  \
###    --atlas_traits PII,MPPI
###
###        For tagging Column:
###   python atlas_associate_tag.py --atlas_server_uri atlas.server.fqdn:port \
###    --atlas_table_FQDN default.students_computers@turing \
###    --atlas_column_name id  \
###    --atlas_traits PII,MPPI
###
### Notes:-
### 1. The script should be able handle both table, column tagging
### 2. Ability to tag multiple traits
### 3. Basic validations like does the tags/traits provided actually exist
### 4. Assumes an unsecure environment, admin/admin access for atlas
### 5. Tested on HDP 2.5
####################################################################################


ATLAS_DOMAIN = "null"


def atlasREST( restAPI ) :
## TODO Verify received code = 200 or else produce an error
    kerberos_auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    url = "https://"+ATLAS_DOMAIN+restAPI
    print ("URL request = %s" %url)
    r= requests.get(url, auth=kerberos_auth, verify=False)
    return(json.loads(r.text));


def atlasPOST( restAPI, data) :
    kerberos_auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    url = "https://"+ATLAS_DOMAIN+restAPI
    print (url)
    r = requests.post(url, auth=kerberos_auth, verify=False ,json=data)
    return (json.loads(r.text));


def parse_args():
  """Atlas Associate Tags: ParseArugument Function."""
  parser = argparse.ArgumentParser()
  parser.description = __doc__
  parser.add_argument('--atlas_server_uri', required=True)
  parser.add_argument('--atlas_table_FQDN', required=True)
  parser.add_argument('--atlas_column_name', required=False)
  parser.add_argument('--atlas_traits', required=True)
  return parser.parse_args()



def print_args(atlas_server_uri, atlas_table_FQDN, atlas_traits):
  """Atlas Associate Tags: Prints All Arguments parsed """
  #print ('Parsed these arguments: %s, %s, %s' % (atlas_server_uri, atlas_table_FQDN, atlas_traits))



def associate_tags_table(atlas_server_uri, atlas_table_FQDN, atlas_traits):
  """Atlas Associate Tags: Tag tables """
  print ('Parsed these arguments: %s, %s, %s' % (atlas_server_uri, atlas_table_FQDN, atlas_traits))
  ####URL format being used to retrive the GUID for the table.
  ####https://atlas.tech.hdp.newyorklife.com/api/atlas/discovery/search/dsl?query=hive_table+where+name=sandbox.tst_test@default
  hive_table_json=atlasREST("/api/atlas/discovery/search/dsl?query=hive_table+where+name=\"%s\"" %(atlas_table_FQDN))
  print(json.dumps(hive_table_json))
  hive_table_id=hive_table_json["results"]["rows"][0]["$id$"]["id"]
  print(json.dumps(hive_table_id))
  trait_list=atlas_traits.split(",")
  for trait in trait_list:
    trait_json = json.loads('{"jsonClass":"org.apache.atlas.typesystem.json.InstanceSerialization$_Struct","typeName":"%s","values":{"name":"addTrait"}}' %(trait))
    print(json.dumps(trait_json))
    updatedTable = atlasPOST("/api/atlas/entities/%s/traits" % (hive_table_id), trait_json)




def associate_tags_column(atlas_server_uri, atlas_table_FQDN, atlas_column_name, atlas_traits):
  """Atlas Associate Tags: Tag Columns """
  print ('Parsed these arguments: %s, %s, %s, %s' % (atlas_server_uri, atlas_table_FQDN, atlas_column_name, atlas_traits))
  ###atlas_column_FQDN = string.split(atlas_table_FQDN,"@")[0]+"."+atlas_column_name+"@"+string.split(atlas_table_FQDN,"@")[1]
  ####hive_column_json=atlasREST("/api/atlas/entities?type=hive_column&property=qualifiedName&value=%s" % (atlas_column_FQDN))
  hive_table_json=atlasREST("/api/atlas/discovery/search/dsl?query=hive_table+where+name=\"%s\"" %(atlas_table_FQDN))
  hive_table_columns_json=hive_table_json["results"]["rows"][0]["columns"]
  for element in hive_table_json["results"]["rows"][0]["columns"]:
  ##print(json.dumps(element["name"]))
    if element["name"] == atlas_column_name:
      print(element["name"])
      hive_column_id=element['$id$']['id']
    else:
      print("element not found %s and %s" %(element["name"], atlas_column_name))
  ##hive_column_id=hive_column_json['definition']['id']['id']
  trait_list=atlas_traits.split(",")
  for trait in trait_list:
    trait_json = json.loads('{"jsonClass":"org.apache.atlas.typesystem.json.InstanceSerialization$_Struct","typeName":"%s","values":{"name":"addTrait"}}' %(trait))
    print (json.dumps(trait_json))
    updatedTable = atlasPOST("/api/atlas/entities/%s/traits" % (hive_column_id), trait_json)




def validate_tags(atlas_traits):
  trait_list=atlas_traits.split(",")
  flag_found = 0
  flag_exit = 0
  types_json = atlasREST("/api/atlas/types")
  print (json.dumps(types_json['results']))


  for trait in trait_list:
    print (trait)
    for element in types_json['results']:
      flag_found = 0
      if (element == trait):
        flag_found = 1
        break


    if (flag_found == 0):
      print ("No trait %s found" % (trait))
      flag_exit = 1
      continue
    else:
      print ("Trait %s found, continue validation" % (trait))


  if (flag_exit == 1):
    print ("ERROR: One or multiple traits not found in Atlas!! Exiting")
    exit(1)
  else:
    print ("All traits specified have been found in Atlas. Continue to tagging")




def main():
  args = parse_args()
  global ATLAS_DOMAIN
  ATLAS_DOMAIN = args.atlas_server_uri
  print_args(
      args.atlas_server_uri,
      args.atlas_table_FQDN,
      args.atlas_traits)


  validate_tags(args.atlas_traits)


  if args.atlas_column_name is not None:
    associate_tags_column(
      args.atlas_server_uri,
      args.atlas_table_FQDN,
      args.atlas_column_name,
      args.atlas_traits)
  else:
    associate_tags_table(
      args.atlas_server_uri,
      args.atlas_table_FQDN,
      args.atlas_traits)
if __name__ == '__main__':
  main()

