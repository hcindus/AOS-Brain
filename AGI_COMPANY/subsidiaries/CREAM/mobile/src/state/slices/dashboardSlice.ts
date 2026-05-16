import {createSlice, createAsyncThunk, PayloadAction} from '@reduxjs/toolkit';
import {api} from '../../api/client';

interface DashboardData {
  leads: number;
  appointments: number;
  revenue: number;
  deals_closed: number;
  conversion_rate: number;
  tasks: string[];
}

interface DashboardState {
  data: DashboardData | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: DashboardState = {
  data: null,
  isLoading: false,
  error: null,
};

export const fetchDashboard = createAsyncThunk(
  'dashboard/fetchDashboard',
  async (_, {rejectWithValue}) => {
    try {
      const response = await api.get('/dashboard');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch dashboard');
    }
  },
);

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(fetchDashboard.pending, state => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDashboard.fulfilled, (state, action: PayloadAction<DashboardData>) => {
        state.isLoading = false;
        state.data = action.payload;
      })
      .addCase(fetchDashboard.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export default dashboardSlice.reducer;
