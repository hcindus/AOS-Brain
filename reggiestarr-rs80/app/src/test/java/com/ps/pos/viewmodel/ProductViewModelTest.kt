package com.ps.pos.viewmodel

import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import com.ps.pos.data.entities.Product
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Rule
import org.junit.Test

@ExperimentalCoroutinesApi
class ProductViewModelTest {

    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    private val testDispatcher = StandardTestDispatcher()
    private lateinit var viewModel: ProductViewModel

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        viewModel = ProductViewModel()
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `initial products list is not empty`() = runTest {
        val products = viewModel.products.value
        assertFalse(products.isEmpty())
        assertEquals(8, products.size) // Sample products
    }

    @Test
    fun `onSearchQueryChange filters products`() = runTest {
        viewModel.onSearchQueryChange("Coca")
        testDispatcher.scheduler.advanceUntilIdle()

        val products = viewModel.products.value
        assertEquals(1, products.size)
        assertEquals("Coca-Cola 20oz", products.first().name)
    }

    @Test
    fun `onSearchQueryChange with blank shows all products`() = runTest {
        viewModel.onSearchQueryChange("Coca")
        testDispatcher.scheduler.advanceUntilIdle()

        viewModel.onSearchQueryChange("")
        testDispatcher.scheduler.advanceUntilIdle()

        val products = viewModel.products.value
        assertEquals(8, products.size)
    }

    @Test
    fun `onSearchQueryChange is case insensitive`() = runTest {
        viewModel.onSearchQueryChange("coca")
        testDispatcher.scheduler.advanceUntilIdle()

        val products = viewModel.products.value
        assertEquals(1, products.size)
    }

    @Test
    fun `searchQuery state updates correctly`() = runTest {
        viewModel.onSearchQueryChange("test query")
        assertEquals("test query", viewModel.searchQuery.value)
    }

    @Test
    fun `search filters by PLU code`() = runTest {
        viewModel.onSearchQueryChange("1001")
        testDispatcher.scheduler.advanceUntilIdle()

        val products = viewModel.products.value
        assertEquals(1, products.size)
        assertEquals("Coca-Cola 20oz", products.first().name)
    }

    @Test
    fun `search with no matches returns empty list`() = runTest {
        viewModel.onSearchQueryChange("xyz123")
        testDispatcher.scheduler.advanceUntilIdle()

        val products = viewModel.products.value
        assertTrue(products.isEmpty())
    }
}