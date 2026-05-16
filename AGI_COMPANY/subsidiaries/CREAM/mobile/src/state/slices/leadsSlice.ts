import {createSlice, createAsyncThunk, PayloadAction} from '@reduxjs/toolkit';
import {api} from '../../api/client';

interface Lead {
  id: number;
  name: string;
  email: string | null;
  phone: string | null;
  source: string;
  status: string;
  temperature: string;
  city: string | null;
  ai_score: number | null;
}

interface LeadsState {
  leads: Lead[];
  isLoading: boolean;
  error: string | null;
}

const initialState: LeadsState = {
  leads: [],
  isLoading: false,
  error: null,
};

export const fetchLeads = createAsyncThunk('leads/fetchLeads', async (_, {rejectWithValue}) => {
  try {
    const response = await api.get('/leads');
    return response.data.leads;
  } catch (error: any) {
    return rejectWithValue(error.response?.data?.detail || 'Failed to fetch leads');
  }
});

export const createLead = createAsyncThunk(
  'leads/createLead',
  async (leadData: Partial<Lead>, {rejectWithValue}) => {
    try {
      const response = await api.post('/leads', leadData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create lead');
    }
  },
);

const leadsSlice = createSlice({
  name: 'leads',
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(fetchLeads.pending, state => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchLeads.fulfilled, (state, action: PayloadAction<Lead[]>) => {
        state.isLoading = false;
        state.leads = action.payload;
      })
      .addCase(fetchLeads.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      .addCase(createLead.fulfilled, (state, action) => {
        state.leads.unshift(action.payload);
      });
  },
});

export default leadsSlice.reducer;
