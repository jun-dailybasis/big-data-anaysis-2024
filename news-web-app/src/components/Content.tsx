import { useState }  from 'react'; // import

import { getAnalytics, logEvent } from "firebase/analytics"; // 1 analytics 들어간다

import {useLocation, useNavigate } from "react-router-dom";
// URL 변경할떄... 썻떤 컴포넌트 import 했다. 
// [1]검색어 눌렸을 때 URL이 바뀌게 parameter가 추가되는 것을 해보자. 

import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Tooltip from '@mui/material/Tooltip';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import RefreshIcon from '@mui/icons-material/Refresh';
import NewsTrendChart from './NewsTrendChart';




export default function Content() {
  const analytics = getAnalytics(); // 2 analytics 들어간다
  const navigate = useNavigate();
  const{ pathname, search } = useLocation();
  // search -> URL ? 뒤에 있는 값들 저장 

  const params = new URLSearchParams(search);
  const searchText = params.get('search') || "";  // 비어있으면 ""로 출력해줘



  const [inputText, setInputText] = useState(""); // 변수 선언


  // handler.
  function onSearch() {

    console.log(`onSearch: ${inputText}` )

    var url = pathname;  // 현재 경로를 넣어준 것. 

    if(inputText) {
      url += `?search=${inputText}`;



    }

    logEvent(analytics, "search", {inputText}); // 3 analytics 들어간다
    navigate(url); // navgigate 이동해라. 

  }


  return (
    <Paper sx={{ maxWidth: 936, margin: 'auto', overflow: 'hidden' }}>
      <AppBar
        position="static"
        color="default"
        elevation={0}
        sx={{ borderBottom: '1px solid rgba(0, 0, 0, 0.12)' }}
      >
        <Toolbar>
          <Grid container spacing={2} sx={{ alignItems: 'center' }}>
            <Grid item>
              <SearchIcon color="inherit" sx={{ display: 'block' }} />
            </Grid>
            <Grid item xs>
              <TextField
                fullWidth
                placeholder="Search by Keywords"
                InputProps={{
                  disableUnderline: true,
                  sx: { fontSize: 'default' },
                }}

                variant="standard" // 붙였다.
                value = {inputText}
                onChange = {(e) => {
                  
                  console.log(e.target.value) ; // 내가 받은 이벤트를 출력 하겠어.
                  // e.target.value 에 글자가 찍힌다. 오.... 

                  // inputText = e.target.value 하면 안된다...
                  setInputText(e.target.value); // 내가 스테이트 값을 바꾸고 있다.
                  //화면에 다가 다시 그려야한다...
                  //state를 바꿀 때는 글자를 변수에 그냥 넣는게 아니라, setInputText

                }}

                onKeyDown ={ (e) => {

                  if(e.key === 'Enter') {
                      onSearch(); // Enter누르면 onSearch 함수가 수행되도록 해줘. 
                  }

                }}



              />
            </Grid>
            <Grid item>
              <Button variant="contained" sx={{ mr: 1 }} onClick = {onSearch}>
                Search
              </Button>
              <Tooltip title="Reload">
                <IconButton>
                  <RefreshIcon color="inherit" sx={{ display: 'block' }} />
                </IconButton>
              </Tooltip>
            </Grid>
          </Grid>
        </Toolbar>
      </AppBar>
     
      <NewsTrendChart search = {searchText}></NewsTrendChart>
    </Paper>
  );
}
