export type SearchReqParams = {
    search : string;
    
};



export type NewsTrendsItem = {
    date : string;
    doc_count : number;



};


export type NewsTrends = {
    trends: NewsTrendsItem[];

}