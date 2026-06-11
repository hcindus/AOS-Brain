package com.psdepot.appointments.ui.screens

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
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.psdepot.appointments.ui.theme.*
import com.psdepot.appointments.ui.viewmodel.ForgotPasswordViewModel
import com.psdepot.appointments.ui.viewmodel.ForgotPasswordState

@Composable
fun ForgotPasswordScreen(
    onNavigateBack: () -> Unit,
    onNavigateToLogin: () -> Unit,
    viewModel: ForgotPasswordViewModel = hiltViewModel()
) {
    var email by remember { mutableStateOf("") }
    var securityAnswer by remember { mutableStateOf("") }
    var showSecurityQuestion by remember { mutableStateOf(false) }
    
    val forgotPasswordState by viewModel.forgotPasswordState.collectAsState()
    val snackbarHostState = remember { SnackbarHostState() }
    val emailFocusRequester = remember { FocusRequester() }
    val securityFocusRequester = remember { FocusRequester() }

    // Handle states
    LaunchedEffect(forgotPasswordState) {
        when (forgotPasswordState) {
            is ForgotPasswordState.Success -> {
                // Email sent successfully
            }
            is ForgotPasswordState.Error -> {
                val message = (forgotPasswordState as ForgotPasswordState.Error).message
                snackbarHostState.showSnackbar(message)
                viewModel.clearError()
            }
            is ForgotPasswordState.RequiresSecurityQuestion -> {
                showSecurityQuestion = true
                securityFocusRequester.requestFocus()
            }
            else -> {}
        }
    }

    LaunchedEffect(Unit) {
        emailFocusRequester.requestFocus()
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = BackgroundPrimary,
        topBar = {
            TopAppBar(
                title = { Text("Reset Password", color = TextPrimary) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back",
                            tint = PSDCyan
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = BackgroundPrimary
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 24.dp, vertical = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            when (forgotPasswordState) {
                is ForgotPasswordState.Success -> SuccessContent(
                    email = email,
                    onNavigateToLogin = onNavigateToLogin,
                    onResend = { viewModel.requestReset(email, securityAnswer) }
                )
                else -> RequestContent(
                    email = email,
                    onEmailChange = { 
                        email = it
                        viewModel.clearError()
                    },
                    securityAnswer = securityAnswer,
                    onSecurityAnswerChange = { securityAnswer = it },
                    showSecurityQuestion = showSecurityQuestion,
                    securityQuestion = if (forgotPasswordState is ForgotPasswordState.RequiresSecurityQuestion) {
                        (forgotPasswordState as ForgotPasswordState.RequiresSecurityQuestion).question
                    } else "",
                    isLoading = forgotPasswordState is ForgotPasswordState.Loading,
                    onSubmit = { viewModel.requestReset(email, securityAnswer) },
                    emailFocusRequester = emailFocusRequester,
                    securityFocusRequester = securityFocusRequester
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Security Footer
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
    }
}

@Composable
private fun RequestContent(
    email: String,
    onEmailChange: (String) -> Unit,
    securityAnswer: String,
    onSecurityAnswerChange: (String) -> Unit,
    showSecurityQuestion: Boolean,
    securityQuestion: String,
    isLoading: Boolean,
    onSubmit: () -> Unit,
    emailFocusRequester: FocusRequester,
    securityFocusRequester: FocusRequester
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Header
        Icon(
            imageVector = Icons.Default.LockReset,
            contentDescription = null,
            tint = PSDCyan,
            modifier = Modifier.size(64.dp)
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = "Forgot your password?",
            style = MaterialTheme.typography.headlineSmall,
            color = TextPrimary,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "Enter your email address and we'll send you a secure link to reset your password.",
            color = TextSecondary,
            textAlign = TextAlign.Center,
            fontSize = 14.sp
        )

        Spacer(modifier = Modifier.height(32.dp))

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
                onNext = { 
                    if (showSecurityQuestion) {
                        securityFocusRequester.requestFocus()
                    } else {
                        onSubmit()
                    }
                }
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
                unfocusedLabelColor = TextMuted
            ),
            shape = RoundedCornerShape(12.dp)
        )

        // Security Question (if required)
        AnimatedVisibility(
            visible = showSecurityQuestion,
            enter = fadeIn(),
            exit = fadeOut()
        ) {
            Column {
                Spacer(modifier = Modifier.height(16.dp))

                Surface(
                    color = BackgroundTertiary,
                    shape = RoundedCornerShape(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Default.Security,
                            contentDescription = null,
                            tint = PSDOrange,
                            modifier = Modifier.size(20.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = securityQuestion,
                            color = TextSecondary,
                            fontSize = 14.sp
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                OutlinedTextField(
                    value = securityAnswer,
                    onValueChange = onSecurityAnswerChange,
                    label = { Text("Your Answer") },
                    leadingIcon = { 
                        Icon(
                            Icons.Default.QuestionMark, 
                            contentDescription = null, 
                            tint = PSDCyan 
                        ) 
                    },
                    keyboardOptions = KeyboardOptions(
                        imeAction = ImeAction.Done
                    ),
                    keyboardActions = KeyboardActions(
                        onDone = { onSubmit() }
                    ),
                    singleLine = true,
                    modifier = Modifier
                        .fillMaxWidth()
                        .focusRequester(securityFocusRequester),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = PSDCyan,
                        focusedLabelColor = PSDCyan,
                        cursorColor = PSDCyan,
                        unfocusedBorderColor = BorderDefault,
                        unfocusedLabelColor = TextMuted
                    ),
                    shape = RoundedCornerShape(12.dp)
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Submit Button
        Button(
            onClick = onSubmit,
            modifier = Modifier
                .fillMaxWidth()
                .height(52.dp),
            enabled = !isLoading && email.isNotBlank() && 
                     (!showSecurityQuestion || securityAnswer.isNotBlank()),
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
                    text = if (showSecurityQuestion) "Verify & Send" else "Send Reset Link",
                    color = PSDDark,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.SemiBold
                )
            }
        }
    }
}

@Composable
private fun SuccessContent(
    email: String,
    onNavigateToLogin: () -> Unit,
    onResend: () -> Unit
) {
    var resendEnabled by remember { mutableStateOf(true) }
    var resendTimer by remember { mutableStateOf(0) }

    LaunchedEffect(resendTimer) {
        if (resendTimer > 0) {
            kotlinx.coroutines.delay(1000)
            resendTimer--
            if (resendTimer == 0) resendEnabled = true
        }
    }

    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Success Icon
        Surface(
            shape = RoundedCornerShape(50),
            color = SuccessBackground,
            modifier = Modifier.size(80.dp)
        ) {
            Box(contentAlignment = Alignment.Center) {
                Icon(
                    imageVector = Icons.Default.MarkEmailRead,
                    contentDescription = null,
                    tint = SuccessColor,
                    modifier = Modifier.size(40.dp)
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        Text(
            text = "Check Your Email",
            style = MaterialTheme.typography.headlineSmall,
            color = TextPrimary,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "We've sent a password reset link to",
            color = TextSecondary,
            textAlign = TextAlign.Center,
            fontSize = 14.sp
        )

        Spacer(modifier = Modifier.height(4.dp))

        Text(
            text = email,
            color = PSDCyan,
            fontWeight = FontWeight.Medium,
            fontSize = 16.sp
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "The link will expire in 30 minutes.",
            color = TextMuted,
            fontSize = 12.sp
        )

        Spacer(modifier = Modifier.height(32.dp))

        // Tips Card
        Surface(
            color = BackgroundTertiary,
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp)
            ) {
                Text(
                    text = "Didn't receive it?",
                    color = TextPrimary,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 14.sp
                )

                Spacer(modifier = Modifier.height(12.dp))

                TipItem("Check your spam/junk folder")
                TipItem("Make sure the email address is correct")
                TipItem("Wait a few minutes for delivery")
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Actions
        Button(
            onClick = onNavigateToLogin,
            modifier = Modifier
                .fillMaxWidth()
                .height(52.dp),
            colors = ButtonDefaults.buttonColors(containerColor = PSDCyan),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text(
                text = "Back to Sign In",
                color = PSDDark,
                fontSize = 16.sp,
                fontWeight = FontWeight.SemiBold
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        TextButton(
            onClick = {
                if (resendEnabled) {
                    resendEnabled = false
                    resendTimer = 60
                    onResend()
                }
            },
            enabled = resendEnabled,
            colors = ButtonDefaults.textButtonColors(
                contentColor = PSDCyan,
                disabledContentColor = TextMuted
            )
        ) {
            Text(
                text = if (resendEnabled) "Resend Email" else "Resend in ${resendTimer}s",
                fontWeight = FontWeight.Medium
            )
        }
    }
}

@Composable
private fun TipItem(text: String) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier.padding(vertical = 4.dp)
    ) {
        Icon(
            imageVector = Icons.Default.CheckCircle,
            contentDescription = null,
            tint = SuccessColor,
            modifier = Modifier.size(16.dp)
        )
        Spacer(modifier = Modifier.width(8.dp))
        Text(
            text = text,
            color = TextSecondary,
            fontSize = 13.sp
        )
    }
}