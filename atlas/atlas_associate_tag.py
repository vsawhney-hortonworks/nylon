#!/usr/bin/python
import argparse
from atlas_api import *

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


def parse_args():
  """Atlas Associate Tags: ParseArugument Function."""
  parser = argparse.ArgumentParser()
  parser.description = __doc__
  parser.add_argument('--atlas_server_uri', required=True)
  parser.add_argument('--atlas_table_FQDN', required=True)
  parser.add_argument('--atlas_traits', required=True)

  return parser.parse_args()

def print_args(atlas_server_uri, atlas_table_FQDN, atlas_traits):
  """Atlas Associate Tags: Prints All Arguments parsed """
  #print ('Parsed these arguments: %s, %s, %s' % (atlas_server_uri, atlas_table_FQDN, atlas_traits))

def associate_tags(atlas_server_uri, atlas_table_FQDN, atlas_traits):
  """Atlas Associate Tags: Prints All Arguments parsed """
  print ('Parsed these arguments: %s, %s, %s' % (atlas_server_uri, atlas_table_FQDN, atlas_traits))
  hive_table_json=atlasREST("/api/atlas/entities?type=hive_table&property=qualifiedName&value=%s" % (atlas_table_FQDN))
  hive_table_id=hive_table_json['definition']['id']['id']
  trait_list=atlas_traits.split(",")
  for trait in trait_list:
    print (trait)
    trait_json=json.loads('{"jsonClass":"org.apache.atlas.typesystem.json.InstanceSerialization$_Struct","typeName":"%s","values":{"name":"addTrait"}}' %(trait))
    updatedTable = atlasPOST("/api/atlas/entities/%s/traits" % (hive_table_id), trait_json)

def main():
  args = parse_args()
  print_args(
      args.atlas_server_uri,
      args.atlas_table_FQDN,
      args.atlas_traits)

  associate_tags(
      args.atlas_server_uri,
      args.atlas_table_FQDN,
      args.atlas_traits)

if __name__ == '__main__':
  main()

