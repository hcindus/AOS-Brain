package com.psdepot.appointments.ui.screens

import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.fragment.app.FragmentActivity
import com.psdepot.appointments.ui.theme.*
import com.psdepot.appointments.ui.viewmodel.*
import kotlinx.coroutines.launch

@Composable
fun LoginScreen(
    onLoginSuccess: () -> Unit,
    onNavigateToRegister: () -> Unit,
    onNavigateToForgotPassword: () -> Unit,
    viewModel: LoginViewModel = hiltViewModel()
) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    val scope = rememberCoroutineScope()

    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var passwordVisible by remember { mutableStateOf(false) }
    var rememberMe by remember { mutableStateOf(false) }

    val loginState by viewModel.loginState.collectAsState()
    val biometricState by viewModel.biometricState.collectAsState()

    val snackbarHostState = remember { SnackbarHostState() }
    val emailFocusRequester = remember { FocusRequester() }
    val passwordFocusRequester = remember { FocusRequester() }

    // Biometric prompt setup
    val biometricPrompt = remember {
        BiometricPrompt(
            context as FragmentActivity,
            lifecycleOwner,
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                    viewModel.loginWithBiometric()
                }

                override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                    scope.launch {
                        snackbarHostState.showSnackbar(errString.toString())
                    }
                }

                override fun onAuthenticationFailed() {
                    scope.launch {
                        snackbarHostState.showSnackbar("Biometric authentication failed")
                    }
                }
            }
        )
    }

    // Handle login states
    LaunchedEffect(loginState) {
        when (loginState) {
            is LoginState.Success -> {
                onLoginSuccess()
            }
            is LoginState.Error -> {
                val message = (loginState as LoginState.Error).message
                snackbarHostState.showSnackbar(message)
                viewModel.clearError()
            }
            is LoginState.BiometricPrompt -> {
                val promptInfo = BiometricPrompt.PromptInfo.Builder()
                    .setTitle("Biometric Authentication")
                    .setSubtitle("Sign in using your biometric credential")
                    .setNegativeButtonText("Cancel")
                    .setConfirmationRequired(false)
                    .build()
                biometricPrompt.authenticate(promptInfo)
            }
            else -> {}
        }
    }

    LaunchedEffect(Unit) {
        emailFocusRequester.requestFocus()
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = BackgroundPrimary
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            // Brand Header
            BrandHeader()

            Spacer(modifier = Modifier.height(40.dp))

            // Login Form
            LoginForm(
                email = email,
                onEmailChange = { 
                    email = it
                    viewModel.clearError()
                },
                password = password,
                onPasswordChange = { 
                    password = it
                    viewModel.clearError()
                },
                passwordVisible = passwordVisible,
                onTogglePasswordVisibility = { passwordVisible = !passwordVisible },
                rememberMe = rememberMe,
                onRememberMeChange = { 
                    rememberMe = it
                    viewModel.setRememberMe(it)
                },
                onLoginClick = { viewModel.login(email, password) },
                onNavigateToForgotPassword = onNavigateToForgotPassword,
                isLoading = loginState is LoginState.Loading,
                emailFocusRequester = emailFocusRequester,
                passwordFocusRequester = passwordFocusRequester
            )

            Spacer(modifier = Modifier.height(24.dp))

            // Biometric Button
            AnimatedVisibility(
                visible = biometricState is BiometricState.Available,
                enter = fadeIn(),
                exit = fadeOut()
            ) {
                BiometricLoginButton(
                    onClick = {
                        val promptInfo = BiometricPrompt.PromptInfo.Builder()
                            .setTitle("Biometric Authentication")
                            .setSubtitle("Sign in using your biometric credential")
                            .setNegativeButtonText("Cancel")
                            .setConfirmationRequired(false)
                            .build()
                        biometricPrompt.authenticate(promptInfo)
                    }
                )
            }

            Spacer(modifier = Modifier.height(32.dp))

            // Divider
            AuthDivider()

            Spacer(modifier = Modifier.height(24.dp))

            // Register Link
            RegisterLink(onNavigateToRegister)

            Spacer(modifier = Modifier.height(24.dp))

            // Security Footer
            SecurityFooter()
        }
    }
}

@Composable
private fun BrandHeader() {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Row(
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "PSD",
                fontSize = 40.sp,
                fontWeight = FontWeight.Bold,
                color = PSDCyan
            )
            Text(
                text = "Appointments",
                fontSize = 40.sp,
                fontWeight = FontWeight.Light,
                color = PSDOrange
            )
        }
        Text(
            text = "Performance Supply Depot",
            fontSize = 14.sp,
            color = TextMuted,
            modifier = Modifier.padding(top = 4.dp)
        )
    }
}

@Composable
private fun LoginForm(
    email: String,
    onEmailChange: (String) -> Unit,
    password: String,
    onPasswordChange: (String) -> Unit,
    passwordVisible: Boolean,
    onTogglePasswordVisibility: () -> Unit,
    rememberMe: Boolean,
    onRememberMeChange: (Boolean) -> Unit,
    onLoginClick: () -> Unit,
    onNavigateToForgotPassword: () -> Unit,
    isLoading: Boolean,
    emailFocusRequester: FocusRequester,
    passwordFocusRequester: FocusRequester
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Email Field
        OutlinedTextField(
            value = email,
            onValueChange = onEmailChange,
            label = { Text("Email Address") },
            leadingIcon = {
                Icon(
                    Icons.Default.Email,
                    contentDescription = null,
                    tint = PSDCyan
                )
            },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Email,
                imeAction = ImeAction.Next
            ),
            keyboardActions = KeyboardActions(
                onNext = { passwordFocusRequester.requestFocus() }
            ),
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .focusRequester(emailFocusRequester),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = PSDCyan,
                focusedLabelColor = PSDCyan,
                cursorColor = PSDCyan,
                unfocusedBorderColor = BorderDefault,
                unfocusedLabelColor = TextMuted,
                unfocusedLeadingIconColor = TextMuted
            ),
            shape = RoundedCornerShape(12.dp)
        )

        // Password Field
        OutlinedTextField(
            value = password,
            onValueChange = onPasswordChange,
            label = { Text("Password") },
            leadingIcon = {
                Icon(
                    Icons.Default.Lock,
                    contentDescription = null,
                    tint = PSDCyan
                )
            },
            trailingIcon = {
                IconButton(onClick = onTogglePasswordVisibility) {
                    Icon(
                        imageVector = if (passwordVisible) 
                            Icons.Default.VisibilityOff 
                        else 
                            Icons.Default.Visibility,
                        contentDescription = "Toggle password visibility",
                        tint = TextMuted
                    )
                }
            },
            visualTransformation = if (passwordVisible) 
                VisualTransformation.None 
            else 
                PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Password,
                imeAction = ImeAction.Done
            ),
            keyboardActions = KeyboardActions(
                onDone = { onLoginClick() }
            ),
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .focusRequester(passwordFocusRequester),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = PSDCyan,
                focusedLabelColor = PSDCyan,
                cursorColor = PSDCyan,
                unfocusedBorderColor = BorderDefault,
                unfocusedLabelColor = TextMuted,
                unfocusedLeadingIconColor = TextMuted
            ),
            shape = RoundedCornerShape(12.dp)
        )

        // Remember Me and Forgot Password
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Checkbox(
                    checked = rememberMe,
                    onCheckedChange = onRememberMeChange,
                    colors = CheckboxDefaults.colors(
                        checkedColor = PSDCyan,
                        uncheckedColor = BorderDefault
                    )
                )
                Text(
                    text = "Remember me",
                    color = TextSecondary,
                    fontSize = 14.sp
                )
            }

            TextButton(
                onClick = onNavigateToForgotPassword,
                colors = ButtonDefaults.textButtonColors(
                    contentColor = PSDCyan
                )
            ) {
                Text("Forgot password?")
            }
        }

        // Login Button
        Button(
            onClick = onLoginClick,
            modifier = Modifier
                .fillMaxWidth()
                .height(52.dp),
            enabled = !isLoading && email.isNotBlank() && password.isNotBlank(),
            colors = ButtonDefaults.buttonColors(
                containerColor = PSDCyan,
                disabledContainerColor = PSDCyan.copy(alpha = 0.5f)
            ),
            shape = RoundedCornerShape(12.dp)
        ) {
            if (isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp),
                    color = PSDDark,
                    strokeWidth = 2.dp
                )
            } else {
                Text(
                    text = "Sign In",
                    color = PSDDark,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.SemiBold
                )
            }
        }
    }
}

@Composable
private fun BiometricLoginButton(onClick: () -> Unit) {
    OutlinedButton(
        onClick = onClick,
        modifier = Modifier
            .fillMaxWidth()
            .height(48.dp),
        border = ButtonDefaults.outlinedButtonBorder.copy(
            brush = androidx.compose.ui.graphics.SolidColor(BorderDefault)
        ),
        shape = RoundedCornerShape(12.dp)
    ) {
        Text(
            text = "Sign in with Biometrics",
            color = TextSecondary,
            fontSize = 14.sp
        )
    }
}

@Composable
private fun AuthDivider() {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Divider(
            modifier = Modifier.weight(1f),
            color = BorderDefault
        )
        Text(
            text = "New to PSD Appointments?",
            color = TextMuted,
            fontSize = 14.sp,
            modifier = Modifier.padding(horizontal = 12.dp)
        )
        Divider(
            modifier = Modifier.weight(1f),
            color = BorderDefault
        )
    }
}

@Composable
private fun RegisterLink(onNavigateToRegister: () -> Unit) {
    Row(
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = "Don't have an account? ",
            color = TextMuted,
            fontSize = 14.sp
        )
        TextButton(
            onClick = onNavigateToRegister,
            colors = ButtonDefaults.textButtonColors(
                contentColor = PSDCyan
            )
        ) {
            Text(
                text = "Create Account",
                fontWeight = FontWeight.SemiBold
            )
        }
    }
}

@Composable
private fun SecurityFooter() {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        Text(
            text = "🔒",
            fontSize = 12.sp
        )
        Spacer(modifier = Modifier.width(4.dp))
        Text(
            text = "Secured with Sentinel-Dusty Auth",
            color = TextMuted,
            fontSize = 12.sp
        )
    }
}