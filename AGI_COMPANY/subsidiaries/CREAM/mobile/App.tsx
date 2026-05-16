import React, {useEffect} from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {Provider as PaperProvider} from 'react-native-paper';
import {SafeAreaProvider} from 'react-native-safe-area-context';
import {Provider as ReduxProvider} from 'react-redux';
import {store} from './src/state/store';
import AppNavigator from './src/navigation/AppNavigator';
import {theme} from './src/constants/theme';
import SplashScreen from 'react-native-splash-screen';

const App = () => {
  useEffect(() => {
    // Hide splash screen after app loads
    // SplashScreen.hide();
  }, []);

  return (
    <ReduxProvider store={store}>
      <PaperProvider theme={theme}>
        <SafeAreaProvider>
          <NavigationContainer>
            <AppNavigator />
          </NavigationContainer>
        </SafeAreaProvider>
      </PaperProvider>
    </ReduxProvider>
  );
};

export default App;
