import { useState } from 'react';
// import {
//   Icon2fa,
//   IconBellRinging,
//   IconDatabaseImport,
//   IconFingerprint,
//   IconKey,
//   IconLogout,
//   IconReceipt2,
//   IconSettings,
//   IconSwitchHorizontal,
// } from "@tabler/icons-react";
import {Container, Group, Grid, Title, Center } from '@mantine/core';
import classes from './dashboard.module.css';
import { Outlet } from 'react-router';


const data = [
  { link: '/dashboard', label: 'Dashboard',icon: "IconBellRinging" },
  { link: 'dashboard/sales', label: 'Sales', icon: "IconReceipt2" },
  { link: '', label: 'Authentication', icon: "Icon2fa" },
  { link: '', label: 'Other Settings', icon: "IconSettings" },
];





export function Dashboard() {

  const [active, setActive] = useState('Billing');


  const links = data.map((item) => (
    <a
      className={classes.link}
      data-active={item.label === active || undefined}
      href={item.link}
      key={item.label}
      onClick={(event) => {
        event.preventDefault();
        setActive(item.label);
      }}
    >
      {/* <item.icon className={classes.linkIcon} stroke={1.5} /> */}
      <span>{item.label}</span>
    </a>
  ));

  return (
    <Grid>
      <Grid.Col span="content">
        <nav className={classes.navbar}>
          <div className={classes.navbarMain}>
            <Group className={classes.header} justify="space-between">
              {/* <MantineLogo size={28} /> */}
              <Title ta={Center}>Vicar</Title>
            </Group>
            {links}
          </div>

          <div className={classes.footer}>
            <a href="#" className={classes.link} onClick={(event) => event.preventDefault()}>
              {/* <IconSwitchHorizontal className={classes.linkIcon} stroke={1.5} /> */}
              <span>Change account</span>
            </a>

            <a href="#" className={classes.link} onClick={(event) => event.preventDefault()}>
              {/* <IconLogout className={classes.linkIcon} stroke={1.5} /> */}
              <span>Logout</span>
            </a>
          </div>
        </nav>
      </Grid.Col>

      <Grid.Col span="auto">
        <Container fluid h={60} style={{
          borderBottom: "2px",
          border: 0,
          borderStyle: "solid",
          borderBlockColor: "black",
        }}>

        </Container>
        <Outlet />
      </Grid.Col>

    </Grid>




  );
}