import { useGetNewsTrendsQuery } from '../app/newsApi';
import Plot from 'react-plotly.js';

import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";

interface IProps {
    search: string;

}

export default function NewsTrendChart({ search } : IProps) {



    const {data, isLoading } = useGetNewsTrendsQuery( { search } ); // 왼쪽 오른쪽 같으면.. 이렇게만 써줘도도돼 search : search

    if(isLoading|| !data){

        return <Box sx = {{p: 3, textAlign: "center"}}>

            <CircularProgress></CircularProgress>

        </Box>
    }
  
    console.log(data);

    const trace: Plotly.Data = {
        x: data.trends.map((x) => x.date),
        y: data.trends.map((x) => x.doc_count),
        type: "scatter",
        mode: "lines+markers",
    }

    return  <Plot
    data={[trace]}
    layout={{autosize:true} }
    style = {{width : "100%", height: "360px"}}
  />

}