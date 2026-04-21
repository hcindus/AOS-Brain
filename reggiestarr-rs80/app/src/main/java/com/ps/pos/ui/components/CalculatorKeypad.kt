package com.ps.pos.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun CalculatorKeypad(
    onDigit: (String) -> Unit,
    onClear: () -> Unit,
    onDelete: () -> Unit,
    onEnter: () -> Unit,
    modifier: Modifier = Modifier
) {
    // Calculator layout: 7-8-9 top, Clear/Enter top row
    Column(modifier = modifier.padding(4.dp)) {
        // Row 1: Clear (spans 2), Enter (spans 2)
        Row(modifier = Modifier.fillMaxWidth()) {
            Button(
                onClick = onClear,
                modifier = Modifier
                    .weight(2f)
                    .padding(2.dp)
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.error
                )
            ) {
                Text("C", style = MaterialTheme.typography.titleLarge)
            }
            Button(
                onClick = onEnter,
                modifier = Modifier
                    .weight(2f)
                    .padding(2.dp)
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary
                )
            ) {
                Text("Enter", style = MaterialTheme.typography.titleMedium)
            }
        }

        // Row 2: 7 8 9
        Row(modifier = Modifier.fillMaxWidth()) {
            listOf("7", "8", "9").forEach { digit ->
                DigitButton(digit, Modifier.weight(1f)) { onDigit(digit) }
            }
        }

        // Row 3: 4 5 6
        Row(modifier = Modifier.fillMaxWidth()) {
            listOf("4", "5", "6").forEach { digit ->
                DigitButton(digit, Modifier.weight(1f)) { onDigit(digit) }
            }
        }

        // Row 4: 1 2 3
        Row(modifier = Modifier.fillMaxWidth()) {
            listOf("1", "2", "3").forEach { digit ->
                DigitButton(digit, Modifier.weight(1f)) { onDigit(digit) }
            }
        }

        // Row 5: . 0 00 Delete
        Row(modifier = Modifier.fillMaxWidth()) {
            DigitButton(".", Modifier.weight(1f)) { onDigit(".") }
            DigitButton("0", Modifier.weight(1f)) { onDigit("0") }
            DigitButton("00", Modifier.weight(1f)) { onDigit("00") }
            IconButton(
                onClick = onDelete,
                modifier = Modifier
                    .weight(1f)
                    .padding(2.dp)
            ) {
                Icon(Icons.Default.ArrowBack, contentDescription = "Delete")
            }
        }
    }
}

@Composable
private fun DigitButton(
    text: String,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    Button(
        onClick = onClick,
        modifier = modifier
            .padding(2.dp)
            .height(64.dp),
        shape = MaterialTheme.shapes.small
    ) {
        Text(
            text,
            style = MaterialTheme.typography.headlineSmall
        )
    }
}
