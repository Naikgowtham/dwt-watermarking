import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { Button } from '../ui/button';
import { Upload, Images, ShieldCheck, LogOut } from 'lucide-react';

const DashboardLayout = () => {
  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  return (
    <div className="flex min-h-screen">
      <aside className="w-64 bg-gray-50 border-r">
        <div className="p-6">
          <h2 className="text-2xl font-bold">Dashboard</h2>
        </div>
        <nav className="flex flex-col p-4">
          <NavLink
            to="/dashboard/upload"
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900 ${
                isActive ? 'bg-gray-200 text-gray-900' : ''
              }`
            }
          >
            <Upload className="h-4 w-4" />
            Upload
          </NavLink>
          <NavLink
            to="/dashboard/creations"
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900 ${
                isActive ? 'bg-gray-200 text-gray-900' : ''
              }`
            }
          >
            <Images className="h-4 w-4" />
            My Creations
          </NavLink>
          <NavLink
            to="/dashboard/verify"
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900 ${
                isActive ? 'bg-gray-200 text-gray-900' : ''
              }`
            }
          >
            <ShieldCheck className="h-4 w-4" />
            Verify
          </NavLink>
        </nav>
        <div className="absolute bottom-0 w-full p-4">
          <Button variant="ghost" className="w-full justify-start" onClick={handleLogout}>
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </div>
      </aside>
      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
  );
};

export default DashboardLayout;
