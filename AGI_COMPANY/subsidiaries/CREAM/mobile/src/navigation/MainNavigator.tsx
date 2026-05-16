import React from 'react';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {IconButton} from 'react-native-paper';
import DashboardScreen from '../screens/dashboard/DashboardScreen';
import LeadsScreen from '../screens/leads/LeadsScreen';
import AppointmentsScreen from '../screens/appointments/AppointmentsScreen';
import RevenueScreen from '../screens/revenue/RevenueScreen';
import ProfileScreen from '../screens/profile/ProfileScreen';

const Tab = createBottomTabNavigator();

const MainNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({route}) => ({
        tabBarIcon: ({color, size}) => {
          let iconName: string;
          switch (route.name) {
            case 'Dashboard':
              iconName = 'view-dashboard';
              break;
            case 'Leads':
              iconName = 'account-group';
              break;
            case 'Appointments':
              iconName = 'calendar';
              break;
            case 'Revenue':
              iconName = 'cash';
              break;
            case 'Profile':
              iconName = 'account';
              break;
            default:
              iconName = 'home';
          }
          return <IconButton icon={iconName} size={size} iconColor={color} />;
        },
        tabBarActiveTintColor: '#1E3A8A',
        tabBarInactiveTintColor: 'gray',
        headerShown: false,
      })}>
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="Leads" component={LeadsScreen} />
      <Tab.Screen name="Appointments" component={AppointmentsScreen} />
      <Tab.Screen name="Revenue" component={RevenueScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
};

export default MainNavigator;
