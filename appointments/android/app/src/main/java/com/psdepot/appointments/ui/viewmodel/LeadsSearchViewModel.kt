package com.psdepot.appointments.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.psdepot.appointments.data.model.LeadInfo
import com.psdepot.appointments.data.repository.AppointmentRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.launch
import javax.inject.Inject

@OptIn(FlowPreview::class)
@HiltViewModel
class LeadsSearchViewModel @Inject constructor(
    private val appointmentRepository: AppointmentRepository
) : ViewModel() {

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    private val _searchResults = MutableStateFlow<List<LeadInfo>>(emptyList())
    val searchResults: StateFlow<List<LeadInfo>> = _searchResults.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _recentSearches = MutableStateFlow<List<String>>(emptyList())
    val recentSearches: StateFlow<List<String>> = _recentSearches.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    init {
        // Debounced search
        viewModelScope.launch {
            _searchQuery
                .debounce(300) // Wait 300ms after typing stops
                .distinctUntilChanged()
                .filter { it.length >= 2 }
                .collect { query ->
                    performSearch(query)
                }
        }

        // Load recent searches from preferences
        loadRecentSearches()
    }

    fun onSearchQueryChange(query: String) {
        _searchQuery.value = query
        if (query.isBlank()) {
            _searchResults.value = emptyList()
        }
    }

    fun performSearch(query: String = _searchQuery.value) {
        if (query.length < 2) {
            _error.value = "Please enter at least 2 characters"
            return
        }

        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null

            appointmentRepository.searchLeads(query)
                .onSuccess { response ->
                    _searchResults.value = response.leads
                    saveRecentSearch(query)
                }
                .onFailure { error ->
                    _error.value = "Search failed: ${error.message}"
                    _searchResults.value = emptyList()
                }

            _isLoading.value = false
        }
    }

    fun clearError() {
        _error.value = null
    }

    private fun loadRecentSearches() {
        // TODO: Load from DataStore/Preferences
        _recentSearches.value = listOf()
    }

    private fun saveRecentSearch(query: String) {
        // TODO: Save to DataStore/Preferences
        val updated = (listOf(query) + _recentSearches.value)
            .distinct()
            .take(5)
        _recentSearches.value = updated
    }
}
