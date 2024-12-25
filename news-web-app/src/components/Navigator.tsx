
import { useLocation, useNavigate } from "react-router-dom";

import Drawer, { DrawerProps } from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ShowChartIcon from '@mui/icons-material/ShowChart'

import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';

import { NEWS_TRENDS_PATH, SENTIMENT_TRENDS_PATH } from '../App';

const item = {
  py: '2px', // padding 여유공간
  px: 3,
  color: 'rgba(255, 255, 255, 0.7)',
  '&:hover, &:focus': {
    bgcolor: 'rgba(255, 255, 255, 0.08)',
  },
};

const itemCategory = {
  boxShadow: '0 -1px 0 rgb(255,255,255,0.1) inset',
  py: 1.5,
  px: 3,
};


export default function Navigator(props: DrawerProps) {
  const { ...other } = props;
  const navigate = useNavigate(); // react Hook 사용법. useNavigate()를 꺼내온다. 

  const { pathname } = useLocation();  // pathname : 현재 경로다.

  const menus = [

  {
    title: 'News Trends',
    path : NEWS_TRENDS_PATH,
    icon : <ShowChartIcon></ShowChartIcon>
    
  },
  { 
    title: 'News Trends',
    path : SENTIMENT_TRENDS_PATH,
    icon : <ShowChartIcon></ShowChartIcon>
  }
  ]

  return (
    <Drawer variant="permanent" {...other}>
      <List disablePadding>

        <ListItem sx={{ ...item, ...itemCategory, fontSize: 22, color: '#fff' }}>
          M E N U.
          </ListItem>

        {

          menus.map(({title, path, icon}) => (
            <ListItem  key ={path} sx={{ ...item, ...itemCategory }}>

              <ListItemButton 
                  selected = { path === pathname } // 현재경로가 path 같으면... selected true

                  onClick={() => {
                  console.log("NEWS_TRENDS_PATH menu")
                  navigate(path)
                  
                  }}>

                <ListItemIcon>
                  {icon}
                </ListItemIcon>

                <ListItemText>{title}</ListItemText>


              </ListItemButton>

            </ListItem>


          ))

        }

       
        
        
      </List>
    </Drawer>
  );
}
