from typing import Dict, Optional, Union
import xml.etree.ElementTree as ET


def extract_fundamentals(xml_data: str) -> Dict[str, Optional[Union[float, str]]]:
    root = ET.fromstring(xml_data)

    fields = {
        "MKTCAP": "market_cap ($ MM)",
        "TTMEBITD": "ebitda ($ MM)",
        "PEEXCLXOR": "pe_ratio",
        "TTMEPSXCLX": "eps",
        "TTMDIVSHR": "dividend_yield",
        "TTMROEPCT": "roe",
        "DEBTTOEQUITY": "debt_to_equity",
        "PRICE2BK": "price_to_book",
        "TTMPR2REV": "price_to_revenue",
        "TTMGROSMGN": "gross_profit_margin",
        "QBVPS": "book_value_ps"
    }

    result: Dict[str, Optional[Union[float, str]]] = {v: None for v in fields.values()}
    
    result["ticker"] = None
    result["company_name"] = None

    coid_elem = root.find(".//CoID[@Type='CompanyName']")
    if coid_elem is not None and coid_elem.text:
        result["company_name"] = coid_elem.text

    for issue in root.findall(".//Issue"):
        ticker_elem = issue.find(".//IssueID[@Type='Ticker']")
        if ticker_elem is not None and ticker_elem.text:
            result["ticker"] = ticker_elem.text
            break

    for ratio in root.iter("Ratio"):
        field = ratio.attrib.get("FieldName")
        text = ratio.text  # Get the text once
        
        if field in fields and text is not None:  # Check for None
            try:
                result[fields[field]] = float(text)
            except (ValueError, TypeError):
                result[fields[field]] = None

    return result


def get_key_fundamental(xml):
    enriched = []

    fund_data = extract_fundamentals(xml)

    enriched_row = {
        "market_cap": fund_data.get("market_cap"),
        "pe_ratio": fund_data.get("pe_ratio"),
        "eps": fund_data.get("eps"),
        "dividend_yield": fund_data.get("dividend_yield"),
        "roe": fund_data.get("roe"),
        "ebitda": fund_data.get("ebitda"),
        "debt_to_equity": fund_data.get("debt_to_equity"),
        "price_to_book": fund_data.get("price_to_book"),
        "price_to_revenue": fund_data.get("price_to_revenue"),
        "book_value_per_share": fund_data.get("book_value_ps"),
        "gross_profit_margin": fund_data.get("gross_profit_margin"),
    }

    enriched.append(enriched_row)

    return enriched