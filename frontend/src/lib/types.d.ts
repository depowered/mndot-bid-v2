declare module 'd3';

type ItemRowData = {
  id: string;
  itemNumber: string;
  itemDescription: string;
  unit: string;
  contractOccur: number;
};

type AvgPriceRowData = {
  category: string;
  wtAvg2018: number;
  wtAvg2019: number;
  wtAvg2020: number;
  wtAvg2021: number;
  wtAvg2022: number;
  wtAvg2023: number;
}

type AvgPriceTableData = {
  headers: string[];
  data: AvgPriceRowData[];
}

type Bid = {
  contractId: number;
  lettingDate: Date;
  bidderName: string;
  quantity: number;
  unitPrice: number;
  category: string;
}