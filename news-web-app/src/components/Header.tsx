import * as React from 'react';

import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
const lightColor = 'rgba(255, 255, 255, 0.7)';

interface HeaderProps {
  onDrawerToggle: () => void;
}

export default function Header(props: HeaderProps) {
  const { onDrawerToggle } = props;

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
                Authentication
              </Typography>
            
        </Toolbar>
      </AppBar>

    </React.Fragment>
  );
}
