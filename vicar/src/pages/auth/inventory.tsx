// import {
//   IconReceipt2,
//   IconArrowDownRight,
//   IconArrowUpRight,
//   IconCoin,
//   IconDiscount2,
//   IconUserPlus,
// } from '@tabler/icons-react';
import { Group, Paper, SimpleGrid, Text, Grid, Table, Avatar, Checkbox, ScrollArea } from '@mantine/core';
import classes from './dashboard.module.css';
import { useState } from 'react';
import cx from 'clsx';


// const icons = {
//   user: "IconUserPlus",
//   discount: "IconDiscount2",
//   receipt: "IconReceipt2",
//   coin: "IconCoin",
// };


// Boxes component 
const statsdata = [
  { title: 'Revenue', icon: 'receipt', value: '13,456', diff: 34 },
  { title: 'Profit', icon: 'coin', value: '4,145', diff: -13 },
  { title: 'Coupons usage', icon: 'discount', value: '745', diff: 18 },
  { title: 'New customers', icon: 'user', value: '188', diff: -30 },
] as const;

const data = [
  {
    id: '1',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-1.png',
    name: 'Robert Wolfkisser',
    job: 'Engineer',
    email: 'rob_wolf@gmail.com',
  },
  {
    id: '2',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-7.png',
    name: 'Jill Jailbreaker',
    job: 'Engineer',
    email: 'jj@breaker.com',
  },
  {
    id: '3',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-2.png',
    name: 'Henry Silkeater',
    job: 'Designer',
    email: 'henry@silkeater.io',
  },
  {
    id: '4',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-3.png',
    name: 'Bill Horsefighter',
    job: 'Designer',
    email: 'bhorsefighter@gmail.com',
  },
  {
    id: '5',
    avatar:
      'https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-10.png',
    name: 'Jeremy Footviewer',
    job: 'Manager',
    email: 'jeremy@foot.dev',
  },
];

export function Inventory() {
  const stats = statsdata.map((stat) => {
    //   const Icon = icons[stat.icon];
    //   const DiffIcon = stat.diff > 0 ? "opened"
    //  : "Closed";

    return (
      <Paper withBorder p="md" radius="md" key={stat.title}>
        <Group justify="space-between">
          <Text size="xs" c="dimmed" className={classes.title}>
            {stat.title}
          </Text>

        </Group>

        <Group align="flex-end" gap="xs" mt={25}>
          <Text className={classes.value}>{stat.value}</Text>
          <Text c={stat.diff > 0 ? 'teal' : 'red'} fz="sm" fw={500} className={classes.diff}>
            <span>{stat.diff}%</span>
            {/* <DiffIcon size={16} stroke={1.5} /> */}
          </Text>
        </Group>

        <Text fz="xs" c="dimmed" mt={7}>
          Compared to previous month
        </Text>
      </Paper>
    );
  });

  const [selection, setSelection] = useState(['1']);
  const toggleRow = (id: string) =>
    setSelection((current) =>
      current.includes(id) ? current.filter((item) => item !== id) : [...current, id]
    );
  const toggleAll = () =>
    setSelection((current) => (current.length === data.length ? [] : data.map((item) => item.id)));

  const rows = data.map((item) => {
    const selected = selection.includes(item.id);
    return (
      <Table.Tr key={item.id} className={cx({ [classes.rowSelected]: selected })} 
      style={{
        marginTop: "2rem"
      }}>
        <Table.Td>
          <Checkbox checked={selection.includes(item.id)} onChange={() => toggleRow(item.id)} />
        </Table.Td>
        <Table.Td>
          <Group gap="sm">
            <Avatar size={26} src={item.avatar} radius={26} />
            <Text size="sm" fw={500}>
              {item.name}
            </Text>
          </Group>
        </Table.Td>
        <Table.Td>{item.email}</Table.Td>
        <Table.Td>{item.job}</Table.Td>
      </Table.Tr>
    );
  });



  return (
    <>

      <Grid.Col span="auto">
        <div className={classes.root}>
          <SimpleGrid cols={{ base: 1, xs: 2, md: 4 }}>{stats}</SimpleGrid>
        </div>



        <ScrollArea>
          <Table miw={800} verticalSpacing="sm">
            <Table.Thead>
              <Table.Tr>
                <Table.Th w={40}>
                  <Checkbox
                    onChange={toggleAll}
                    checked={selection.length === data.length}
                    indeterminate={selection.length > 0 && selection.length !== data.length}
                  />
                </Table.Th>
                <Table.Th>User</Table.Th>
                <Table.Th>Email</Table.Th>
                <Table.Th>Job</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>{rows}</Table.Tbody>
          </Table>
        </ScrollArea>
      </Grid.Col>

    </>




  );
}