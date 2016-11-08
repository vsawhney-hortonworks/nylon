#!/usr/bin/python
import argparse
import requests
import json
import sys
import string

###from atlas_api import *

### python atlas_associate_tag.py --atlas_server_uri xena.hdp.com:21000 --atlas_table_FQDN default.students_computers@turing  --atlas_traits PII,MPPI


##tableFQDN = 'default.students_computers@turing'
##trait='protected'
##print("FIND HIVE_TABLE ENTITY FOR MODIFICATION:")
##hive_table_json=atlasREST("/api/atlas/entities?type=hive_table&property=qualifiedName&value=%s" % (tableFQDN))
##hive_table_id=hive_table_json['definition']['id']['id']

##trait_json=json.loads('{"jsonClass":"org.apache.atlas.typesystem.json.InstanceSerialization$_Struct","typeName":"%s","values":{"name":"addTrait"}}' %(trait))
##print json.dumps(trait_json)
##print json.dumps()
##print ("Updating traits on hive_table %s" % (tableFQDN))
##updatedTable = atlasPOST("/api/atlas/entities/%s/traits" % (hive_table_id), trait_json)
###print traitJson
###print json.dumps(hive_tables, indent=4, sort_keys=True)

ATLAS_DOMAIN="yellow.hdp.com:21000"

def atlasREST( restAPI ) :
## TODO Verify received code = 200 or else produce an error
    url = "http://"+ATLAS_DOMAIN+restAPI
    print "URL request = %s" % (url)
    r= requests.get(url, auth=("admin", "admin"))
    return(json.loads(r.text));


def atlasPOST( restAPI, data) :
    url = "http://" + ATLAS_DOMAIN + restAPI
    print (url)
    r = requests.post(url, auth=("admin", "admin"),json=data)
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
  """Atlas Associate Tags: Prints All Arguments parsed """
  print ('Parsed these arguments: %s, %s, %s' % (atlas_server_uri, atlas_table_FQDN, atlas_traits))
  hive_table_json=atlasREST("/api/atlas/entities?type=hive_table&property=qualifiedName&value=%s" % (atlas_table_FQDN))
  hive_table_id=hive_table_json['definition']['id']['id']
  trait_list=atlas_traits.split(",")
  for trait in trait_list:
    trait_json = json.loads('{"jsonClass":"org.apache.atlas.typesystem.json.InstanceSerialization$_Struct","typeName":"%s","values":{"name":"addTrait"}}' %(trait))
    print json.dumps(trait_json)
    updatedTable = atlasPOST("/api/atlas/entities/%s/traits" % (hive_table_id), trait_json)

def associate_tags_column(atlas_server_uri, atlas_table_FQDN, atlas_column_name, atlas_traits):
  """Atlas Associate Tags: Prints All Arguments parsed """
  print ('Parsed these arguments: %s, %s, %s, %s' % (atlas_server_uri, atlas_table_FQDN, atlas_column_name, atlas_traits))
  atlas_column_FQDN = string.split(atlas_table_FQDN,"@")[0]+"."+atlas_column_name+"@"+string.split(atlas_table_FQDN,"@")[1]
  
  hive_column_json=atlasREST("/api/atlas/entities?type=hive_column&property=qualifiedName&value=%s" % (atlas_column_FQDN))
  hive_column_id=hive_column_json['definition']['id']['id']
  trait_list=atlas_traits.split(",")
  for trait in trait_list:
    trait_json = json.loads('{"jsonClass":"org.apache.atlas.typesystem.json.InstanceSerialization$_Struct","typeName":"%s","values":{"name":"addTrait"}}' %(trait))
    print json.dumps(trait_json)
    updatedTable = atlasPOST("/api/atlas/entities/%s/traits" % (hive_column_id), trait_json)


def validate_tags(atlas_traits):
  trait_list=atlas_traits.split(",")
  flag_found = 0
  flag_exit = 0
  types_json = atlasREST("/api/atlas/types")
  print json.dumps(types_json['results'])
  
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

