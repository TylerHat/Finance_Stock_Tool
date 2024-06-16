import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
import plotly.io as pio
import mpld3 


from finance_strategies.bollingBandsRSI_html import bollingBandsRSI

bollingBandsRSI("META", 365)