/**
 * Sentinel Shield Admin Dashboard
 * React Application
 */

const { useState, useEffect } = React;
const { BrowserRouter, Routes, Route, Link, useNavigate } = ReactRouterDOM;

// API Configuration
const API_BASE = '/api';

// Auth Context
const AuthContext = React.createContext(null);

function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            const response = await fetch(`${API_BASE}/auth/me`, {
                credentials: 'include'
            });
            if (response.ok) {
                const data = await response.json();
                setUser(data.user);
            }
        } catch (err) {
            console.error('Auth check failed:', err);
        } finally {
            setLoading(false);
        }
    };

    const login = async (email, password) => {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            setUser(data.user);
            return { success: true };
        }
        return { success: false, error: 'Invalid credentials' };
    };

    const logout = async () => {
        await fetch(`${API_BASE}/auth/logout`, { 
            method: 'POST',
            credentials: 'include' 
        });
        setUser(null);
        navigate('/login');
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

// Login Page
function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = React.useContext(AuthContext);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const result = await login(email, password);
        if (result.success) {
            navigate('/dashboard');
        } else {
            setError(result.error);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-gray-800">
            <div className="bg-gray-800 p-8 rounded-xl shadow-2xl w-full max-w-md border border-gray-700">
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-blue-500 rounded-xl mx-auto mb-4 flex items-center justify-center">
                        <i data-lucide="shield" className="w-8 h-8 text-white"></i>
                    </div>
                    <h1 className="text-2xl font-bold text-white">Sentinel Shield</h1>
                    <p className="text-gray-400">Admin Dashboard</p>
                </div>
                
                {error && (
                    <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded mb-4">
                        {error}
                    </div>
                )}
                
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
                    >
                        Sign In
                    </button>
                </form>
            </div>
        </div>
    );
}

// Dashboard
function Dashboard() {
    const [stats, setStats] = useState(null);
    const { user } = React.useContext(AuthContext);

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        const response = await fetch(`${API_BASE}/admin/stats`, { credentials: 'include' });
        if (response.ok) {
            const data = await response.json();
            setStats(data);
        }
    };

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <StatCard
                    title="Total Users"
                    value={stats?.totalUsers || 0}
                    icon="users"
                    color="blue"
                />
                <StatCard
                    title="Active Sessions"
                    value={stats?.activeSessions || 0}
                    icon="activity"
                    color="green"
                />
                <StatCard
                    title="Failed Logins (24h)"
                    value={stats?.failedLogins || 0}
                    icon="alert-triangle"
                    color="yellow"
                />
                <StatCard
                    title="Security Alerts"
                    value={stats?.securityAlerts || 0}
                    icon="shield-alert"
                    color="red"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <RecentActivity />
                <SystemHealth />
            </div>
        </div>
    );
}

function StatCard({ title, value, icon, color }) {
    const colorClasses = {
        blue: 'bg-blue-500/20 border-blue-500/30',
        green: 'bg-green-500/20 border-green-500/30',
        yellow: 'bg-yellow-500/20 border-yellow-500/30',
        red: 'bg-red-500/20 border-red-500/30'
    };

    return (
        <div className={`${colorClasses[color]} border rounded-xl p-6`}>
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-gray-400 text-sm">{title}</p>
                    <p className="text-3xl font-bold text-white mt-1">{value.toLocaleString()}</p>
                </div>
                <div className="w-12 h-12 bg-white/10 rounded-lg flex items-center justify-center">
                    <i data-lucide={icon} className="w-6 h-6"></i>
                </div>
            </div>
        </div>
    );
}

// Layout Component
function Layout({ children }) {
    const { user, logout } = React.useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        lucide.createIcons();
    });

    const menuItems = [
        { path: '/dashboard', label: 'Dashboard', icon: 'layout-dashboard' },
        { path: '/users', label: 'Users', icon: 'users' },
        { path: '/sessions', label: 'Sessions', icon: 'key' },
        { path: '/audit', label: 'Audit Logs', icon: 'file-text' },
        { path: '/security', label: 'Security', icon: 'shield' },
        { path: '/settings', label: 'Settings', icon: 'settings' },
    ];

    return (
        <div className="flex h-screen bg-gray-900">
            <aside className="w-64 bg-gray-800 border-r border-gray-700">
                <div className="p-6 border-b border-gray-700">
                    <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                            <i data-lucide="shield" className="w-6 h-6 text-white"></i>
                        </div>
                        <span className="text-xl font-bold">Sentinel</span>
                    </div>
                </div>
                
                <nav className="p-4 space-y-1">
                    {menuItems.map(item => (
                        <Link
                            key={item.path}
                            to={item.path}
                            className="flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-700 transition text-gray-300 hover:text-white"
                        >
                            <i data-lucide={item.icon} className="w-5 h-5"></i>
                            <span>{item.label}</span>
                        </Link>
                    ))}
                </nav>
                
                <div className="absolute bottom-0 left-0 w-64 p-4 border-t border-gray-700">
                    <button
                        onClick={logout}
                        className="flex items-center space-x-3 px-4 py-3 w-full rounded-lg hover:bg-gray-700 transition text-gray-300 hover:text-red-400"
                    >
                        <i data-lucide="log-out" className="w-5 h-5"></i>
                        <span>Sign Out</span>
                    </button>
                </div>
            </aside>
            
            <main className="flex-1 overflow-auto">
                {children}
            </main>
        </div>
    );
}

// User Management
function UserManagement() {
    const [users, setUsers] = useState([]);
    const [search, setSearch] = useState('');

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        const response = await fetch(`${API_BASE}/admin/users`, { credentials: 'include' });
        if (response.ok) {
            const data = await response.json();
            setUsers(data.users);
        }
    };

    const filteredUsers = users.filter(u => 
        u.email.toLowerCase().includes(search.toLowerCase()) ||
        (u.first_name && u.first_name.toLowerCase().includes(search.toLowerCase())) ||
        (u.last_name && u.last_name.toLowerCase().includes(search.toLowerCase()))
    );

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">User Management</h1>
                <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg flex items-center space-x-2">
                    <i data-lucide="plus" className="w-4 h-4"></i>
                    <span>Add User</span>
                </button>
            </div>

            <div className="mb-6">
                <input
                    type="text"
                    placeholder="Search users..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="w-full max-w-md px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
            </div>

            <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
                <table className="w-full">
                    <thead className="bg-gray-700">
                        <tr>
                            <th className="px-6 py-3 text-left text-sm font-medium text-gray-300">User</th>
                            <th className="px-6 py-3 text-left text-sm font-medium text-gray-300">Email</th>
                            <th className="px-6 py-3 text-left text-sm font-medium text-gray-300">Role</th>
                            <th className="px-6 py-3 text-left text-sm font-medium text-gray-300">Status</th>
                            <th className="px-6 py-3 text-left text-sm font-medium text-gray-300">Last Login</th>
                            <th className="px-6 py-3 text-left text-sm font-medium text-gray-300">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-700">
                        {filteredUsers.map(user => (
                            <tr key={user.id} className="hover:bg-gray-700/50">
                                <td className="px-6 py-4">
                                    <div className="flex items-center space-x-3">
                                        <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-sm font-bold">
                                            {user.first_name?.[0] || user.email[0].toUpperCase()}
                                        </div>
                                        <span className="font-medium">{user.first_name} {user.last_name}</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-gray-300">{user.email}</td>
                                <td className="px-6 py-4">
                                    <span className="px-2 py-1 bg-blue-500/20 text-blue-300 rounded text-sm">
                                        {user.role || 'User'}
                                    </span>
                                </td>
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-1 rounded text-sm ${user.active ? 'bg-green-500/20 text-green-300' : 'bg-red-500/20 text-red-300'}`}>
                                        {user.active ? 'Active' : 'Inactive'}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-gray-400 text-sm">
                                    {user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never'}
                                </td>
                                <td className="px-6 py-4">
                                    <button className="text-blue-400 hover:text-blue-300 mr-3">
                                        <i data-lucide="edit-2" className="w-4 h-4"></i>
                                    </button>
                                    <button className="text-red-400 hover:text-red-300">
                                        <i data-lucide="trash-2" className="w-4 h-4"></i>
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

// Main App
function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <Routes>
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/*" element={
                        <Layout>
                            <Routes>
                                <Route path="/dashboard" element={<Dashboard />} />
                                <Route path="/users" element={<UserManagement />} />
                                <Route path="/" element={<Dashboard />} />
                            </Routes>
                        </Layout>
                    } />
                </Routes>
            </AuthProvider>
        </BrowserRouter>
    );
}

// Mount React
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
