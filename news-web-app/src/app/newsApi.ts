import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

import * as t from "./types";

export const newsApi = createApi({
  reducerPath: "news-api",
  baseQuery: fetchBaseQuery({
    baseUrl: "https://i16roxn1pf.execute-api.ap-northeast-2.amazonaws.com/",
  }),
  endpoints: (builder) => ({
    getNewsTrends: builder.query<t.NewsTrends, t.SearchReqParams>({
      //query: (param) => `news-trends?search=${params.search}`,
      query: ({search}) => `news-trends?search=${search}`,
    }),
  }),
});

export const { useGetNewsTrendsQuery } = newsApi;