# Script en Python (pandas) para comparar tarifas PVPC con precios fijos
Este script usa los siguientes datos para comparar precios regulados (PVPC) con precios fijos:
* Histórico de precios PVPC descargados de REE en formato csv.
* Datos horarios del contador eléctrico descargados de la compañía distribuidora en formato csv.
* Datos de facturación de la compañía eléctrica comercializadora (en este caso SOM ENERGIA) pasados a mano a formato csv dede las facturas en formato pdf.

Todos estos ficheros csv se importan en el módulo **pandas** de Python, donde se relizan las operaciones de _slicing_ por fechas de factura y cálculo comparativo por mes.

**NOTA:** Los detalles de formato se pueden ver en los comentarios del código y en los ejemplos de ficheros incluidos en este repo.*

## Código
* `electricdata.py`: Módulo con las funciones que luego se usan en el módulo principal.
* `main.py`: Módulo principal.

