from lxml import etree
from xml.dom.minidom import parse, parseString

url_pub="http://cris.sgul.ac.uk:8090/publications-api/publications/74365"
url_rel_inv="http://cris.sgul.ac.uk:8090/publications-api/relationships?involving=publication(74365)"
url_rel="http://cris.sgul.ac.uk:8090/publications-api/relationships/79822"
url_user="http://cris.sgul.ac.uk:8090/publications-api/users/391"

xml_input = etree.parse(url_rel)
xslt_root = etree.parse("symplectic-to-vivo.datamap.xsl")
transform = etree.XSLT(xslt_root)
rdf_xml = transform(xml_input)


print str(rdf_xml)


