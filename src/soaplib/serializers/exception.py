
#
# soaplib - Copyright (C) Soaplib contributors.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#

from soaplib.serializers import Base

# FIXME: totally untested

class Fault(Exception, Base):
    def __init__(self, faultcode = 'Server', faultstring = None,
                 detail = None, name = 'ExceptionFault'):
        self.faultcode = faultcode
        self.faultstring = faultstring
        self.detail = detail
        self.name = name

    @classmethod
    def to_xml(cls, value, name):
        fault = etree.Element(name)

        etree.SubElement(fault, 'faultcode').text = value.faultcode
        etree.SubElement(fault, 'faultstring').text = value.faultstring
        etree.SubElement(fault, 'detail').text = value.detail

        return fault

    @classmethod
    def from_xml(cls, element):
        code = _element_to_string(element.find('faultcode'))
        string = _element_to_string(element.find('faultstring'))
        detail_element = element.find('detail')
        if detail_element is not None:
            if len(detail_element.getchildren()):
                detail = ElementTree.tostring(detail_element)
            else:
                detail = _element_to_string(element.find('detail'))
        else:
            detail = ''
        return Fault(faultcode=code, faultstring=string, detail=detail)

    def add_to_schema(self, schema_dict):
        complex_type = etree.Element('complexType')
        complex_type.set('name', self.get_datatype())
        sequenceNode = etree.SubElement(complex_type, 'sequence')

        element = etree.SubElement(sequenceNode, 'element')
        element.set('name', 'detail')
        element.set('{%s}type' % _ns_xsi, '{%s}string' % _ns_xs)

        element = etree.SubElement(sequenceNode, 'element')
        element.set('name', 'message')
        element.set('{%s}type' % _ns_xsi, '{%s}string' % _ns_xs)

        schema_dict[self.type_name_ns] = complex_type

        typeElementItem = etree.Element('element')
        typeElementItem.set('name', 'ExceptionFaultType')
        typeElementItem.set('{%s}type' % _ns_xsi, self.get_datatype(nsmap))
        schema_dict['%sElement' % (self.type_name_ns)] = typeElementItem

    def __str__(self):
        io = cStringIO.StringIO()
        io.write("*" * 80)
        io.write("\r\n")
        io.write(" Recieved soap fault \r\n")
        io.write(" FaultCode            %s \r\n" % self.faultcode)
        io.write(" FaultString          %s \r\n" % self.faultstring)
        io.write(" FaultDetail          \r\n")
        if self.detail is not None:
            io.write(self.detail)
        return io.getvalue()