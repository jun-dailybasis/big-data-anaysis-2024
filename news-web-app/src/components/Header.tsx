import * as React from 'react';

import { useLocation } from 'react-router-dom';

import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';


import { NEWS_TRENDS_PATH, SENTIMENT_TRENDS_PATH } from '../App';

interface HeaderProps {
  onDrawerToggle: () => void;
}

export default function Header(props: HeaderProps) {
  
  const { pathname } = useLocation();
  
  function getTitle() {

      switch(pathname){

        case NEWS_TRENDS_PATH:
          return 'News Trends';

        case SENTIMENT_TRENDS_PATH:
          return 'Sentiment Trends';

        default:
          return 'Unknown';

      }

  }


  return (
    <React.Fragment>

      <AppBar
        component="div"
        color="primary"
        position="static"
        elevation={0}
        sx={{ zIndex: 0,
          paddingTop: '16px',
          paddingBottom: '16px'
         }}
      >
        <Toolbar>
        
              <Typography color="inherit" variant="h5" component="h1">
                {getTitle()}
              </Typography>
            
        </Toolbar>
      </AppBar>

    </React.Fragment>
  );
}
