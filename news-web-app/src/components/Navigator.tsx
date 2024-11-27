
import Drawer, { DrawerProps } from '@mui/material/Drawer';
import List from '@mui/material/List';

import ListItem from '@mui/material/ListItem';

import ShowChartIcon from '@mui/icons-material/ShowChart'
import ListItemIcon from '@mui/material/ListItemIcon';

import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';




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

  return (
    <Drawer variant="permanent" {...other}>
      <List disablePadding>

        <ListItem sx={{ ...item, ...itemCategory, fontSize: 22, color: '#fff' }}>
          바꾼다.
          </ListItem>

        <ListItem sx={{ ...item, ...itemCategory }}>
          <ListItemIcon>
            <ShowChartIcon />
          </ListItemIcon>
          <ListItemText>News trend</ListItemText>
        </ListItem>

        <ListItem sx={{ ...item, ...itemCategory }}>
          <ListItemIcon>
            <ShowChartIcon />
          </ListItemIcon>
          <ListItemText>Old Trend</ListItemText>
        </ListItem>

        
        
      </List>
    </Drawer>
  );
}
