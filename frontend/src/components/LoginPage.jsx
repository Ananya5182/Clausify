import React, { useState } from 'react';
import Logo from './Logo';
import { 
  Mail, 
  Lock, 
  Eye, 
  EyeOff, 
  ArrowRight, 
  ShieldCheck, 
  Sparkles, 
  CheckCircle2, 
  Scale, 
  User, 
  Briefcase, 
  Building,
  Check
} from 'lucide-react';

export default function LoginPage({ onLoginSuccess }) {
  const [isSignUp, setIsSignUp] = useState(false);
  const [selectedRole, setSelectedRole] = useState('consumer'); // 'consumer' | 'counsel'
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [barIdOrOrg, setBarIdOrOrg] = useState('');
  const [rememberMe, setRememberMe] = useState(true);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!email || !email.includes('@')) {
      setError('Please provide a valid email address.');
      return;
    }
    if (!password || password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }
    if (isSignUp && !name.trim()) {
      setError('Please enter your full name.');
      return;
    }

    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      const user = {
        name: name.trim() || email.split('@')[0],
        email: email.trim(),
        role: selectedRole, // 'consumer' or 'counsel'
        organization: barIdOrOrg.trim() || (selectedRole === 'counsel' ? 'Independent Legal Counsel' : undefined),
        avatar: `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(name || email)}`,
      };
      if (rememberMe) {
        localStorage.setItem('clausify_user', JSON.stringify(user));
      }
      onLoginSuccess(user);
    }, 600);
  };

  // Quick 1-click Demo Logins for instant evaluation
  const handleQuickDemo = (role = 'consumer') => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      const demoUser = role === 'counsel' ? {
        name: 'Adv. Priya Sharma',
        email: 'priya.sharma@legalshield.org',
        role: 'counsel',
        organization: 'High Court Bar Council / LexAdvocates',
        avatar: 'https://api.dicebear.com/7.x/initials/svg?seed=Priya+Sharma',
      } : {
        name: 'Rahul Verma',
        email: 'rahul.verma@example.com',
        role: 'consumer',
        organization: 'Individual Consumer',
        avatar: 'https://api.dicebear.com/7.x/initials/svg?seed=Rahul+Verma',
      };
      localStorage.setItem('clausify_user', JSON.stringify(demoUser));
      onLoginSuccess(demoUser);
    }, 400);
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4 relative overflow-hidden">
      
      {/* Background Ambient Glow Orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl pointer-events-none -translate-x-1/2 -translate-y-1/2" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none translate-x-1/2 translate-y-1/2" />
      <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-teal-500/5 rounded-full blur-2xl pointer-events-none -translate-x-1/2 -translate-y-1/2" />

      {/* Decorative Grid Mesh */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b15_1px,transparent_1px),linear-gradient(to_bottom,#1e293b15_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] pointer-events-none" />

      <div className="max-w-md w-full relative z-10 py-6">
        
        {/* Logo and Brand Header */}
        <div className="text-center mb-5">
          <div className="inline-block">
            <Logo size="lg" showText={true} subtitle={false} className="justify-center" />
          </div>
          <p className="text-xs text-slate-400 mt-2">
            AI Legal Agreement Scanner & Statutory Grievance Shield
          </p>
        </div>

        {/* Main Glass Card */}
        <div className="glass-panel rounded-3xl p-6 sm:p-7 border border-slate-800 shadow-2xl bg-slate-900/85 backdrop-blur-2xl">
          
          {/* Mode Switcher Tabs: Sign In vs Sign Up */}
          <div className="flex bg-slate-950/80 p-1 rounded-xl border border-slate-800/80 mb-5">
            <button
              type="button"
              onClick={() => { setIsSignUp(false); setError(''); }}
              className={`flex-1 py-2 text-xs font-semibold rounded-lg transition-all ${
                !isSignUp
                  ? 'bg-gradient-to-r from-brand-600 to-emerald-500 text-white shadow-md shadow-brand-500/25'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Sign In
            </button>
            <button
              type="button"
              onClick={() => { setIsSignUp(true); setError(''); }}
              className={`flex-1 py-2 text-xs font-semibold rounded-lg transition-all ${
                isSignUp
                  ? 'bg-gradient-to-r from-brand-600 to-emerald-500 text-white shadow-md shadow-brand-500/25'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Create Account
            </button>
          </div>

          {/* Role Selection: Consumer vs Counsel */}
          <div className="mb-5">
            <label className="text-[11px] font-bold text-slate-300 uppercase tracking-wider block mb-2">
              Select Your Profile Role:
            </label>
            <div className="grid grid-cols-2 gap-2.5">
              
              {/* Option 1: Consumer */}
              <button
                type="button"
                onClick={() => setSelectedRole('consumer')}
                className={`p-3 rounded-2xl border text-left transition-all relative ${
                  selectedRole === 'consumer'
                    ? 'bg-emerald-950/30 border-emerald-500/80 shadow-md shadow-emerald-950/50'
                    : 'bg-slate-950/60 border-slate-800 hover:border-slate-700 text-slate-400'
                }`}
              >
                {selectedRole === 'consumer' && (
                  <span className="absolute top-2 right-2 w-4 h-4 rounded-full bg-emerald-500 text-slate-950 flex items-center justify-center">
                    <Check className="w-3 h-3 stroke-[3]" />
                  </span>
                )}
                <div className="flex items-center gap-2 mb-1">
                  <div className={`p-1.5 rounded-lg ${selectedRole === 'consumer' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-800 text-slate-400'}`}>
                    <User className="w-4 h-4" />
                  </div>
                  <span className={`text-xs font-bold ${selectedRole === 'consumer' ? 'text-emerald-300' : 'text-slate-300'}`}>
                    Consumer
                  </span>
                </div>
                <p className="text-[10px] text-slate-400 leading-tight">
                  Individual user, consumer disputes, personal contracts
                </p>
              </button>

              {/* Option 2: Legal Counsel */}
              <button
                type="button"
                onClick={() => setSelectedRole('counsel')}
                className={`p-3 rounded-2xl border text-left transition-all relative ${
                  selectedRole === 'counsel'
                    ? 'bg-indigo-950/30 border-indigo-500/80 shadow-md shadow-indigo-950/50'
                    : 'bg-slate-950/60 border-slate-800 hover:border-slate-700 text-slate-400'
                }`}
              >
                {selectedRole === 'counsel' && (
                  <span className="absolute top-2 right-2 w-4 h-4 rounded-full bg-indigo-500 text-white flex items-center justify-center">
                    <Check className="w-3 h-3 stroke-[3]" />
                  </span>
                )}
                <div className="flex items-center gap-2 mb-1">
                  <div className={`p-1.5 rounded-lg ${selectedRole === 'counsel' ? 'bg-indigo-500/20 text-indigo-400' : 'bg-slate-800 text-slate-400'}`}>
                    <Scale className="w-4 h-4" />
                  </div>
                  <span className={`text-xs font-bold ${selectedRole === 'counsel' ? 'text-indigo-300' : 'text-slate-300'}`}>
                    Legal Counsel
                  </span>
                </div>
                <p className="text-[10px] text-slate-400 leading-tight">
                  Advocate, lawyer, legal reviewer, corporate counsel
                </p>
              </button>

            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-3.5">
            
            {/* Full Name field (for Sign Up) */}
            {isSignUp && (
              <div>
                <label className="text-[11px] font-semibold text-slate-300 block mb-1">
                  Full Name
                </label>
                <div className="relative">
                  <User className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder={selectedRole === 'counsel' ? 'e.g. Adv. Priya Sharma' : 'e.g. Rahul Verma'}
                    className="w-full pl-9 pr-3 py-2 text-xs rounded-xl bg-slate-950/80 border border-slate-800 text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500"
                  />
                </div>
              </div>
            )}

            {/* Optional Organization / Bar Registration field for Legal Counsel */}
            {isSignUp && selectedRole === 'counsel' && (
              <div>
                <label className="text-[11px] font-semibold text-slate-300 block mb-1">
                  Law Firm / Bar Council ID <span className="text-slate-500 font-normal">(Optional)</span>
                </label>
                <div className="relative">
                  <Briefcase className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                  <input
                    type="text"
                    value={barIdOrOrg}
                    onChange={(e) => setBarIdOrOrg(e.target.value)}
                    placeholder="e.g. High Court Bar Council / LexAdvocates"
                    className="w-full pl-9 pr-3 py-2 text-xs rounded-xl bg-slate-950/80 border border-slate-800 text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
              </div>
            )}

            {/* Email Address */}
            <div>
              <label className="text-[11px] font-semibold text-slate-300 block mb-1">
                Email Address
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="w-full pl-9 pr-3 py-2 text-xs rounded-xl bg-slate-950/80 border border-slate-800 text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-[11px] font-semibold text-slate-300">
                  Password
                </label>
                {!isSignUp && (
                  <button
                    type="button"
                    onClick={() => alert('Password reset instructions sent to your email.')}
                    className="text-[11px] text-brand-400 hover:text-brand-300 transition-colors"
                  >
                    Forgot password?
                  </button>
                )}
              </div>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full pl-9 pr-10 py-2 text-xs rounded-xl bg-slate-950/80 border border-slate-800 text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-2.5 text-slate-500 hover:text-slate-300"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Remember Me Checkbox */}
            <div className="flex items-center justify-between text-xs pt-0.5">
              <label className="flex items-center gap-2 cursor-pointer select-none text-slate-400 hover:text-slate-300">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="rounded border-slate-800 bg-slate-950 text-brand-500 focus:ring-brand-500/30"
                />
                <span>Remember me on this browser</span>
              </label>
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-2.5 rounded-xl bg-red-950/40 border border-red-800/80 text-red-300 text-xs flex items-center gap-2">
                <span>{error}</span>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-2.5 px-4 rounded-xl text-xs font-bold tracking-wide uppercase text-white shadow-lg active:scale-[0.99] transition-all flex items-center justify-center gap-2 cursor-pointer ${
                selectedRole === 'counsel'
                  ? 'bg-gradient-to-r from-indigo-600 via-blue-600 to-emerald-500 shadow-indigo-500/25 hover:from-indigo-500 hover:to-emerald-400'
                  : 'bg-gradient-to-r from-brand-600 via-emerald-500 to-teal-500 shadow-emerald-500/25 hover:from-brand-500 hover:to-emerald-400'
              }`}
            >
              {isLoading ? (
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <span>
                    {isSignUp 
                      ? `Create ${selectedRole === 'counsel' ? 'Counsel' : 'Consumer'} Account` 
                      : `Sign In as ${selectedRole === 'counsel' ? 'Legal Counsel' : 'Consumer'}`}
                  </span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>

          </form>

          {/* Trial & Interface Preview (Demo Sandbox) */}
          <div className="mt-5 pt-4 border-t border-slate-800/80">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[10px] uppercase font-bold tracking-wider text-slate-300 flex items-center gap-1.5">
                <Sparkles className="w-3 h-3 text-amber-400" />
                <span>Interface Preview & Trial Sandbox:</span>
              </span>
              <span className="text-[9px] font-semibold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/20">
                Evaluation Only
              </span>
            </div>

            <p className="text-[11px] text-slate-400 mb-3 leading-relaxed">
              These 1-click demo profiles are provided for a <strong>trial period</strong> to showcase how the interface, clause scanner, and grievance notice generator function. To handle actual disputes or review real client agreements, please <strong>Sign In</strong> or <strong>Create an Account</strong> above.
            </p>

            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => handleQuickDemo('consumer')}
                className="flex items-center justify-center gap-1.5 py-2 px-2.5 rounded-xl bg-slate-950/80 hover:bg-slate-900 border border-slate-800 hover:border-emerald-500/40 text-slate-300 hover:text-emerald-300 text-[11px] font-medium transition-all group cursor-pointer"
              >
                <User className="w-3.5 h-3.5 text-emerald-400 group-hover:scale-110 transition-transform" />
                <span>Try Demo Consumer</span>
              </button>
              <button
                type="button"
                onClick={() => handleQuickDemo('counsel')}
                className="flex items-center justify-center gap-1.5 py-2 px-2.5 rounded-xl bg-slate-950/80 hover:bg-slate-900 border border-slate-800 hover:border-indigo-500/40 text-slate-300 hover:text-indigo-300 text-[11px] font-medium transition-all group cursor-pointer"
              >
                <Scale className="w-3.5 h-3.5 text-indigo-400 group-hover:scale-110 transition-transform" />
                <span>Try Demo Counsel</span>
              </button>
            </div>
          </div>

          {/* Privacy & Compliance Assurance */}
          <div className="mt-4 flex items-center justify-center gap-1.5 text-[11px] text-slate-400">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>256-bit Encrypted Session & Zero Data Reselling</span>
          </div>

        </div>

        {/* Role Comparison Explainer Cards */}
        <div className="mt-4 grid grid-cols-2 gap-2.5 text-[11px] text-slate-400">
          <div className="p-2.5 rounded-xl bg-slate-900/40 border border-slate-800/60">
            <span className="font-semibold text-emerald-400 flex items-center gap-1 mb-0.5">
              <User className="w-3 h-3" /> Consumer Mode
            </span>
            <span>Simplified legal language, refund dispute redressal & personal notices.</span>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-900/40 border border-slate-800/60">
            <span className="font-semibold text-indigo-400 flex items-center gap-1 mb-0.5">
              <Scale className="w-3 h-3" /> Counsel Mode
            </span>
            <span>Statutory section citations, contract risk auditing & advocate representation.</span>
          </div>
        </div>

      </div>

    </div>
  );
}
