import pandas as pd 

def create_table( filename, caption):
    id = filename.split(".")[0]
    data = pd.read_csv(filename, sep='\t')
    sorteddf = data.sort_values('pval',ascending=True)
    htmlout = "<h4 align=\"center\">Function Enrichment in " + caption +"</h4>"
    htmlout += "<div style=\"height: 850px; width: 600px; border: 1px ridge; black; background: #e9d8f2; padding-top: 20px; padding-right: 0px; padding-bottom: 20px; padding-left: 20px; overflow: auto;\"><table id=\"" + id + "\" class=\"table table-striped table-bordered\" style=\"width:100%\"><thead><tr><th>Feature Id</th><th>Term</th><th>Matches</th><th>P-value</th></tr></thead><tbody>"
    
    for index, row in sorteddf.iterrows():
       feature = row['ID']
       term = row['Term']
       matches = row['k']
       pvalue = format(row["pval"], '.3g')
       htmlout += "<tr><td>" + feature + "</td><td>" + term + "</td><td>" + str(matches) + "</td><td>" + str(pvalue) + "</td></tr>"
    htmlout += "</tbody><tfoot><tr><th>Feature Id</th><th>Term</th><th>Matches</th><th>P-value</th></tr></tfoot></table></div>"
    return htmlout

def generate_html(outputdir):
   outfile = outputdir + "/output.html"
   
   output = "<html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\"><link rel=\"stylesheet\" type=\"text/css \"href=\"https:// cdn.datatables.net/1.10.20/css/dataTables.bootstrap.min.css\"><script src=\"https://code.jquery.com/jquery-3.3.1.js\"></script><script src=\"https://cdn.datatables.net/1.10.20/js/ jquery.dataTables.min.js\"></script><script src=\"https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap.min.js\"></script>"


   output += "<script> $(document).ready(function() {$(\'#go_biological_process_output\').DataTable();} ); </script>"
   output += "<script> $(document).ready(function() {$(\'#go_molecular_function_output\').DataTable();} ); </script>"
   output += "<script> $(document).ready(function() {$(\'#go_cellular_component_output\').DataTable();} ); </script>"
   output += "<script> $(document).ready(function() {$(\'#kegg_enzyme_output\').DataTable();} ); </script>"
   output += "<script> $(document).ready(function() {$(\'#kog_output\').DataTable();} ); </script>"
   output += "<script> $(document).ready(function() {$(\'#panther_output\').DataTable();} ); </script>"
   output += "<script> $(document).ready(function() {$(\'#smart_output\').DataTable();} ); </script>"
   output += "<script> $(document).ready(function() {$(\'#pfam_output\').DataTable();} ); </script>"
   output += "<script> $(document).ready(function() {$(\'#pathway_output\').DataTable();} ); </script>"
   output += "</head><body><table cellpadding = \"100\" cellspacing = \"100\" >"



   output += "<tr><td>" + create_table("go_biological_process_output.txt", "GO Biological Process") + "</td><td>" + create_table("go_molecular_function_output.txt", "GO Molecular Function") + "</td> <td>" + create_table("go_cellular_component_output.txt", "GO Cellular Component") + "</td></tr>"

   output += "<tr><td>" + create_table("kegg_enzyme_output.txt", "KEGG Enzyme") + "</td> <td>" + create_table("kog_output.txt", "KOG") + "</td> <td>" + create_table("panther_output.txt", "Panther") + "</td></tr>"

   output += "<tr><td>" + create_table("smart_output.txt", "SMART") + "</td> <td>" + create_table("pfam_output.txt", "PFAM") + "</td> <td>" + create_table("pathway_output.txt", "Pathway") + "</td></tr>"

   output += "</table></body></html>"
    
   print(output)

   fout = open(outfile, "w")
   fout.write(output)
   fout.close()

generate_html("/home/manish/Desktop/GeneSet_Enrichment/data/167")

