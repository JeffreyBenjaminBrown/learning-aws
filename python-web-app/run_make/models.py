from django . db import models


class TaxConfig ( models . Model ):
  vatRate = models . FloatField ( "VAT rate",
                                  default = 0.19 )
  incomeTaxRate = models . FloatField ( "income tax rate",
                                        default = 0 )
