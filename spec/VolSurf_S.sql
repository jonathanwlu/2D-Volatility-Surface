
select TDaysToExp TDTE, Strike, avg(HedgeVol) IV, avg(PrevIVol) pIV, avg(StockPrice) sPx, avg(pStockPrice) pPx
from
(
select *
from tblOptions
where Symbol = 'SPY'
and ESSRoot = ''
and TDaysToExp > 4
and ImpliedVol > 0
and Strike < 1.1*StockPrice
and Strike > 0.5*StockPrice
and CP = 'P'
and abs(HedgeDelta) >= 0.1

union all

select *
from tblOptions
where Symbol = 'SPY'
and ESSRoot = ''
and TDaysToExp > 4
and ImpliedVol > 0
and Strike > 0.9*StockPrice
and Strike < 1.5*StockPrice
and CP = 'C'
and abs(HedgeDelta) >= 0.1

) a
group by TDaysToExp, Strike
order by TDaysToExp, Strike

