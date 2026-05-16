import React, {useState} from 'react';
import {View, StyleSheet, KeyboardAvoidingView, Platform, ScrollView} from 'react-native';
import {TextInput, Button, Text, Surface} from 'react-native-paper';
import {useDispatch, useSelector} from 'react-redux';
import {login, clearError} from '../../state/slices/authSlice';
import {RootState} from '../../state/store';

const LoginScreen = ({navigation}: any) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [secureText, setSecureText] = useState(true);
  const dispatch = useDispatch();
  const {isLoading, error} = useSelector((state: RootState) => state.auth);

  const handleLogin = () => {
    dispatch(clearError());
    dispatch(login({email, password}) as any);
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Surface style={styles.card} elevation={2}>
          <View style={styles.header}>
            <Text style={styles.logoIcon}>🏠</Text>
            <Text style={styles.title}>CREAM</Text>
            <Text style={styles.subtitle}>Capitalize Real Estate Asset Management</Text>
          </View>

          {error && (
            <Text style={styles.error}>{error}</Text>
          )}

          <TextInput
            label="Email"
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
            keyboardType="email-address"
            style={styles.input}
            mode="outlined"
          />

          <TextInput
            label="Password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry={secureText}
            right={<TextInput.Icon icon={secureText ? 'eye' : 'eye-off'} onPress={() => setSecureText(!secureText)} />}
            style={styles.input}
            mode="outlined"
          />

          <Button
            mode="contained"
            onPress={handleLogin}
            loading={isLoading}
            disabled={isLoading || !email || !password}
            style={styles.button}>
            Sign In
          </Button>

          <Button
            mode="text"
            onPress={() => navigation.navigate('Register')}
            style={styles.linkButton}>
            Don't have an account? Get started
          </Button>

          <Text style={styles.demoText}>Demo: demo@cream.app / demo123</Text>
        </Surface>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1E3A8A',
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
  },
  card: {
    padding: 24,
    borderRadius: 16,
    backgroundColor: '#fff',
  },
  header: {
    alignItems: 'center',
    marginBottom: 24,
  },
  logoIcon: {
    fontSize: 48,
    marginBottom: 8,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1E3A8A',
  },
  subtitle: {
    fontSize: 14,
    color: '#6B7280',
    textAlign: 'center',
  },
  input: {
    marginBottom: 16,
  },
  button: {
    marginTop: 8,
    paddingVertical: 8,
  },
  linkButton: {
    marginTop: 8,
  },
  error: {
    color: '#EF4444',
    marginBottom: 16,
    textAlign: 'center',
  },
  demoText: {
    marginTop: 16,
    textAlign: 'center',
    color: '#6B7280',
    fontSize: 12,
  },
});

export default LoginScreen;
