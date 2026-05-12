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
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.psdepot.appointments.ui.theme.*
import com.psdepot.appointments.ui.viewmodel.*

@Composable
fun RegisterScreen(
    onRegistrationComplete: () -> Unit,
    onNavigateBack: () -> Unit,
    viewModel: RegisterViewModel = hiltViewModel()
) {
    var currentStep by remember { mutableStateOf(1) }
    val registerState by viewModel.registerState.collectAsState()
    val snackbarHostState = remember { SnackbarHostState() }

    // Handle registration state
    LaunchedEffect(registerState) {
        when (registerState) {
            is RegisterState.Success -> onRegistrationComplete()
            is RegisterState.Error -> {
                snackbarHostState.showSnackbar((registerState as RegisterState.Error).message)
                viewModel.clearError()
            }
            is RegisterState.ValidationError -> {
                snackbarHostState.showSnackbar((registerState as RegisterState.ValidationError).message)
                viewModel.clearError()
            }
            is RegisterState.Step1Complete -> currentStep = 2
            else -> {}
        }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = BackgroundPrimary,
        topBar = {
            TopAppBar(
                title = { Text("Create Account", color = TextPrimary) },
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
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Step Indicator
            StepIndicator(currentStep = currentStep)

            Spacer(modifier = Modifier.height(32.dp))

            when (currentStep) {
                1 -> StepOneForm(
                    viewModel = viewModel,
                    onNext = { viewModel.validateStep1() }
                )
                2 -> StepTwoForm(
                    viewModel = viewModel,
                    onBack = { currentStep = 1 },
                    onSubmit = { viewModel.register() },
                    isLoading = registerState is RegisterState.Loading
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
private fun StepIndicator(currentStep: Int) {
    Row(
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically
    ) {
        StepCircle(
            number = 1,
            label = "Account",
            isActive = currentStep == 1,
            isCompleted = currentStep > 1
        )
        
        StepConnector(isCompleted = currentStep > 1)
        
        StepCircle(
            number = 2,
            label = "Company",
            isActive = currentStep == 2,
            isCompleted = false
        )
    }
}

@Composable
private fun StepCircle(
    number: Int,
    label: String,
    isActive: Boolean,
    isCompleted: Boolean
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Surface(
            shape = RoundedCornerShape(50),
            color = when {
                isCompleted -> SuccessColor
                isActive -> PSDCyan
                else -> BackgroundTertiary
            },
            modifier = Modifier.size(36.dp)
        ) {
            Box(contentAlignment = Alignment.Center) {
                if (isCompleted) {
                    Icon(
                        imageVector = Icons.Default.Check,
                        contentDescription = null,
                        tint = PSDDark,
                        modifier = Modifier.size(20.dp)
                    )
                } else {
                    Text(
                        text = number.toString(),
                        color = if (isActive) PSDDark else TextMuted,
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 14.sp
                    )
                }
            }
        }
        Spacer(modifier = Modifier.height(4.dp))
        Text(
            text = label,
            color = if (isActive || isCompleted) TextPrimary else TextMuted,
            fontSize = 12.sp
        )
    }
}

@Composable
private fun StepConnector(isCompleted: Boolean) {
    Box(
        modifier = Modifier
            .width(40.dp)
            .height(2.dp)
            .padding(horizontal = 4.dp)
    ) {
        Surface(
            color = if (isCompleted) SuccessColor else BorderDefault,
            modifier = Modifier.fillMaxSize()
        ) {}
    }
}

@Composable
private fun StepOneForm(
    viewModel: RegisterViewModel,
    onNext: () -> Unit
) {
    var passwordVisible by remember { mutableStateOf(false) }
    var confirmPasswordVisible by remember { mutableStateOf(false) }
    val focusRequesters = List(5) { remember { FocusRequester() } }

    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Email
        OutlinedTextField(
            value = viewModel.email,
            onValueChange = { viewModel.email = it },
            label = { Text("Email Address *") },
            leadingIcon = { Icon(Icons.Default.Email, null, tint = PSDCyan) },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Email,
                imeAction = ImeAction.Next
            ),
            keyboardActions = KeyboardActions(
                onNext = { focusRequesters[1].requestFocus() }
            ),
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .focusRequester(focusRequesters[0]),
            colors = outlinedTextFieldColors(),
            shape = RoundedCornerShape(12.dp)
        )

        // First & Last Name Row
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            OutlinedTextField(
                value = viewModel.firstName,
                onValueChange = { viewModel.firstName = it },
                label = { Text("First Name *") },
                leadingIcon = { Icon(Icons.Default.Person, null, tint = PSDCyan) },
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
                keyboardActions = KeyboardActions(
                    onNext = { focusRequesters[2].requestFocus() }
                ),
                singleLine = true,
                modifier = Modifier
                    .weight(1f)
                    .focusRequester(focusRequesters[1]),
                colors = outlinedTextFieldColors(),
                shape = RoundedCornerShape(12.dp)
            )

            OutlinedTextField(
                value = viewModel.lastName,
                onValueChange = { viewModel.lastName = it },
                label = { Text("Last Name *") },
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
                keyboardActions = KeyboardActions(
                    onNext = { focusRequesters[3].requestFocus() }
                ),
                singleLine = true,
                modifier = Modifier
                    .weight(1f)
                    .focusRequester(focusRequesters[2]),
                colors = outlinedTextFieldColors(),
                shape = RoundedCornerShape(12.dp)
            )
        }

        // Password
        PasswordFieldWithStrength(
            value = viewModel.password,
            onValueChange = { viewModel.password = it },
            label = "Password *",
            passwordVisible = passwordVisible,
            onToggleVisibility = { passwordVisible = !passwordVisible },
            focusRequester = focusRequesters[3],
            onNext = { focusRequesters[4].requestFocus() }
        )

        // Confirm Password
        OutlinedTextField(
            value = viewModel.confirmPassword,
            onValueChange = { viewModel.confirmPassword = it },
            label = { Text("Confirm Password *") },
            leadingIcon = { Icon(Icons.Default.Lock, null, tint = PSDCyan) },
            trailingIcon = {
                IconButton(onClick = { confirmPasswordVisible = !confirmPasswordVisible }) {
                    Icon(
                        imageVector = if (confirmPasswordVisible) 
                            Icons.Default.VisibilityOff 
                        else 
                            Icons.Default.Visibility,
                        contentDescription = "Toggle",
                        tint = TextMuted
                    )
                }
            },
            visualTransformation = if (confirmPasswordVisible) 
                VisualTransformation.None 
            else 
                PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Password,
                imeAction = ImeAction.Done
            ),
            keyboardActions = KeyboardActions(
                onDone = { onNext() }
            ),
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .focusRequester(focusRequesters[4]),
            colors = outlinedTextFieldColors(),
            shape = RoundedCornerShape(12.dp)
        )

        // Terms Checkbox
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth()
        ) {
            Checkbox(
                checked = viewModel.acceptTerms,
                onCheckedChange = { viewModel.acceptTerms = it },
                colors = CheckboxDefaults.colors(
                    checkedColor = PSDCyan,
                    uncheckedColor = BorderDefault
                )
            )
            Text(
                text = "I agree to the Terms of Service and Privacy Policy *",
                color = TextSecondary,
                fontSize = 13.sp
            )
        }

        // Continue Button
        Button(
            onClick = onNext,
            modifier = Modifier
                .fillMaxWidth()
                .height(52.dp),
            colors = ButtonDefaults.buttonColors(containerColor = PSDCyan),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text(
                text = "Continue",
                color = PSDDark,
                fontSize = 16.sp,
                fontWeight = FontWeight.SemiBold
            )
        }
    }
}

@Composable
private fun StepTwoForm(
    viewModel: RegisterViewModel,
    onBack: () -> Unit,
    onSubmit: () -> Unit,
    isLoading: Boolean
) {
    val focusRequesters = List(5) { remember { FocusRequester() } }

    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Company Name
        OutlinedTextField(
            value = viewModel.companyName,
            onValueChange = { viewModel.companyName = it },
            label = { Text("Company Name *") },
            leadingIcon = { Icon(Icons.Default.Business, null, tint = PSDCyan) },
            keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
            keyboardActions = KeyboardActions(
                onNext = { focusRequesters[1].requestFocus() }
            ),
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .focusRequester(focusRequesters[0]),
            colors = outlinedTextFieldColors(),
            shape = RoundedCornerShape(12.dp)
        )

        // Phone and Industry Row
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            OutlinedTextField(
                value = viewModel.companyPhone,
                onValueChange = { viewModel.companyPhone = it },
                label = { Text("Phone") },
                leadingIcon = { Icon(Icons.Default.Phone, null, tint = PSDCyan) },
                keyboardOptions = KeyboardOptions(
                    keyboardType = KeyboardType.Phone,
                    imeAction = ImeAction.Next
                ),
                singleLine = true,
                modifier = Modifier.weight(1f),
                colors = outlinedTextFieldColors(),
                shape = RoundedCornerShape(12.dp)
            )

            // Industry Dropdown
            var expanded by remember { mutableStateOf(false) }
            ExposedDropdownMenuBox(
                expanded = expanded,
                onExpandedChange = { expanded = it },
                modifier = Modifier.weight(1f)
            ) {
                OutlinedTextField(
                    value = viewModel.industry,
                    onValueChange = {},
                    label = { Text("Industry") },
                    readOnly = true,
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                    modifier = Modifier.menuAnchor(),
                    colors = outlinedTextFieldColors(),
                    shape = RoundedCornerShape(12.dp)
                )
                ExposedDropdownMenu(
                    expanded = expanded,
                    onDismissRequest = { expanded = false }
                ) {
                    listOf("POS Supplies", "Retail", "Hospitality", "Healthcare", "Technology", "Other")
                        .forEach { option ->
                            DropdownMenuItem(
                                text = { Text(option) },
                                onClick = {
                                    viewModel.industry = option
                                    expanded = false
                                }
                            )
                        }
                }
            }
        }

        // Address
        OutlinedTextField(
            value = viewModel.companyAddress,
            onValueChange = { viewModel.companyAddress = it },
            label = { Text("Business Address") },
            leadingIcon = { Icon(Icons.Default.LocationOn, null, tint = PSDCyan) },
            keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
            minLines = 2,
            maxLines = 3,
            modifier = Modifier.fillMaxWidth(),
            colors = outlinedTextFieldColors(),
            shape = RoundedCornerShape(12.dp)
        )

        // Website
        OutlinedTextField(
            value = viewModel.companyWebsite,
            onValueChange = { viewModel.companyWebsite = it },
            label = { Text("Website") },
            leadingIcon = { Icon(Icons.Default.Language, null, tint = PSDCyan) },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Uri,
                imeAction = ImeAction.Done
            ),
            keyboardActions = KeyboardActions(
                onDone = { onSubmit() }
            ),
            singleLine = true,
            modifier = Modifier.fillMaxWidth(),
            colors = outlinedTextFieldColors(),
            shape = RoundedCornerShape(12.dp)
        )

        // Newsletter
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth()
        ) {
            Checkbox(
                checked = viewModel.subscribeNewsletter,
                onCheckedChange = { viewModel.subscribeNewsletter = it },
                colors = CheckboxDefaults.colors(
                    checkedColor = PSDCyan,
                    uncheckedColor = BorderDefault
                )
            )
            Text(
                text = "Subscribe to product updates and industry news",
                color = TextSecondary,
                fontSize = 13.sp
            )
        }

        // Buttons
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            OutlinedButton(
                onClick = onBack,
                modifier = Modifier.weight(0.4f).height(52.dp),
                border = ButtonDefaults.outlinedButtonBorder.copy(
                    brush = androidx.compose.ui.graphics.SolidColor(BorderDefault)
                ),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("Back", color = TextSecondary)
            }

            Button(
                onClick = onSubmit,
                modifier = Modifier.weight(0.6f).height(52.dp),
                enabled = !isLoading,
                colors = ButtonDefaults.buttonColors(containerColor = PSDCyan),
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
                        text = "Create Account",
                        color = PSDDark,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.SemiBold
                    )
                }
            }
        }
    }
}

@Composable
private fun PasswordFieldWithStrength(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    passwordVisible: Boolean,
    onToggleVisibility: () -> Unit,
    focusRequester: FocusRequester,
    onNext: () -> Unit
) {
    Column {
        OutlinedTextField(
            value = value,
            onValueChange = onValueChange,
            label = { Text(label) },
            leadingIcon = { Icon(Icons.Default.Lock, null, tint = PSDCyan) },
            trailingIcon = {
                IconButton(onClick = onToggleVisibility) {
                    Icon(
                        imageVector = if (passwordVisible) 
                            Icons.Default.VisibilityOff 
                        else 
                            Icons.Default.Visibility,
                        contentDescription = "Toggle",
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
                imeAction = ImeAction.Next
            ),
            keyboardActions = KeyboardActions(onNext = { onNext() }),
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .focusRequester(focusRequester),
            colors = outlinedTextFieldColors(),
            shape = RoundedCornerShape(12.dp)
        )

        if (value.isNotEmpty()) {
            PasswordStrengthIndicator(password = value)
        }
    }
}

@Composable
private fun PasswordStrengthIndicator(password: String) {
    val requirements = listOf(
        "length" to (password.length >= 8),
        "uppercase" to password.any { it.isUpperCase() },
        "lowercase" to password.any { it.isLowerCase() },
        "number" to password.any { it.isDigit() },
        "special" to password.any { !it.isLetterOrDigit() }
    )

    val metCount = requirements.count { it.second }
    val strengthColor = when {
        metCount >= 5 -> SuccessColor
        metCount >= 3 -> WarningColor
        else -> ErrorColor
    }

    Column(modifier = Modifier.padding(top = 8.dp)) {
        // Strength Bar
        LinearProgressIndicator(
            progress = { metCount / 5f },
            modifier = Modifier
                .fillMaxWidth()
                .height(4.dp),
            color = strengthColor,
            trackColor = BorderDefault
        )

        Spacer(modifier = Modifier.height(8.dp))

        // Requirements
        Column {
            requirements.forEach { (req, met) ->
                val (icon, text) = when (req) {
                    "length" -> Icons.Default.Check to "At least 8 characters"
                    "uppercase" -> Icons.Default.Check to "One uppercase letter"
                    "lowercase" -> Icons.Default.Check to "One lowercase letter"
                    "number" -> Icons.Default.Check to "One number"
                    "special" -> Icons.Default.Check to "One special character"
                    else -> Icons.Default.Check to ""
                }

                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.padding(vertical = 2.dp)
                ) {
                    Icon(
                        imageVector = if (met) Icons.Default.CheckCircle else Icons.Default.RadioButtonUnchecked,
                        contentDescription = null,
                        tint = if (met) SuccessColor else TextMuted,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = text,
                        color = if (met) TextSecondary else TextMuted,
                        fontSize = 12.sp
                    )
                }
            }
        }
    }
}

@Composable
private fun outlinedTextFieldColors() = OutlinedTextFieldDefaults.colors(
    focusedBorderColor = PSDCyan,
    focusedLabelColor = PSDCyan,
    cursorColor = PSDCyan,
    unfocusedBorderColor = BorderDefault,
    unfocusedLabelColor = TextMuted,
    unfocusedLeadingIconColor = TextMuted
)