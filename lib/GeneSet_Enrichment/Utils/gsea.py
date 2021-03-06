import sys
import os
import json
import uuid
from scipy.stats import hypergeom

class gsea:
  def __init__(self):
      pass

  def find_kbase_phytozome_genome_id(self, ws, genome_ref_id):
    
    '''
    Input a KBase genome ref
    Output: 
     return Phytozome genome name in KBase
     return 0 if not a phytozome genome / copy of phytozome genome
    '''
    
    #exit(type(ws))
    provenance = ws.get_object_provenance([{"ref":genome_ref_id}])
    original_ws_id = provenance[0]['orig_wsid']
    original_workspace_name  = ws.get_workspace_info({'id':original_ws_id})[1]
    print (genome_ref_id + "\t" + original_workspace_name)

    if original_workspace_name != 'Phytozome_Genomes':
        return 0

    provenance = ws.get_object_provenance([{"ref":genome_ref_id}])

    if 'copied' in provenance[0]:
        copied = True
        
    while (copied==True):
        provenance = ws.get_object_provenance([{"ref":genome_ref_id}])

        if 'copied' in provenance[0]:
            copied = True
            genome_ref_id = provenance[0]['copied']
            #print genome_ref_id
        else:
            copied = False

    phytozome_obj_name = ws.get_object_info3({'objects': [{'ref': genome_ref_id}]})['infos'][0][1]

    return phytozome_obj_name
  
  def run_gsea(self, featurename, gene_file, outdirectory):      
      
      association_file = "/kb/module/data/167/167_" + featurename + ".gmt"
      
      feature_dict = {}
      gene_feature = {}
      feature_term = {}
      
      try:
         fassoc = open(association_file, "r")
         
         for line in fassoc:
           line = line.rstrip()
           id = line.split("\t")
           feature_id = id[1]
           num_fields = len(id)
           feature_dict[feature_id] = num_fields - 2
           feature_term[feature_id] = id[0]
           for i in range(3, num_fields):
               gene_id = id[i]

               if gene_id not in gene_feature:
                  feature_value = []
                  feature_value.append(feature_id) 
                  gene_feature[gene_id] = feature_value
               else:
                  gene_feature[gene_id].append(feature_id)
         fassoc.close()

      except IOError:
            print ('cannot open', association_file)
            fassoc.close()
      

      N = len(gene_feature.keys())

      n = 0
      featurefreq = {}

      try:
         fgene = open(gene_file, "r")
         for gline in fgene:
           gline = gline.rstrip()
           n += 1
           geneids = gline.split(",")

           if geneids[0] in gene_feature:
              feature_list = gene_feature[geneids[0]]

              for feature in feature_list: 
                  if feature in featurefreq:
                     featurefreq[feature] += 1 
                  else:
                     featurefreq[feature] = 1

         fout= open(outdirectory + "/" + featurename + "_output.txt","a")
         fout.write("ID\tTerm\tN\tK\tn\tk\tpval\n")
         for feature_key, frequency in featurefreq.items():
             k = frequency
             K = feature_dict[feature_key]
             prb = hypergeom.pmf(k, N, K, n)
           
             fout.write (feature_key + "\t"+ (feature_term[feature_key]).split("_")[1] +"\t" + str(N) + "\t" + str(K) + "\t" + str(n) + "\t" + str(k) + "\t" +str(format(prb, '.3g')) + "\n")
         fout.close()
         fgene.close()
    
      except IOError:
              print ('cannot open', gene_file)
              fgene.close()
      
      return (outdirectory)

      
  
