import React from 'react';
import classNames from 'classnames';

const DashboardCard = ({ title, value, icon: Icon, trend, trendValue, color = 'primary' }) => {
    return (
        <div className="glass-card p-6 relative overflow-hidden group hover:bg-slate-800/60 transition-all duration-300">
            {/* Background Gradient Blob */}
            <div className={classNames(
                "absolute -top-10 -right-10 w-32 h-32 rounded-full blur-3xl opacity-20 group-hover:opacity-30 transition-opacity",
                color === 'primary' ? 'bg-primary-500' :
                    color === 'secondary' ? 'bg-secondary-500' :
                        color === 'emerald' ? 'bg-emerald-500' : 'bg-orange-500'
            )} />

            <div className="relative z-10">
                <div className="flex justify-between items-start mb-4">
                    <div className={classNames(
                        "p-3 rounded-xl",
                        color === 'primary' ? 'bg-primary-500/10 text-primary-400' :
                            color === 'secondary' ? 'bg-secondary-500/10 text-secondary-400' :
                                color === 'emerald' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-orange-500/10 text-orange-400'
                    )}>
                        <Icon size={24} />
                    </div>
                    {trend && (
                        <div className={classNames(
                            "flex items-center text-sm font-medium",
                            trend === 'up' ? 'text-emerald-400' : 'text-rose-400'
                        )}>
                            <span>{trend === 'up' ? '+' : ''}{trendValue}</span>
                        </div>
                    )}
                </div>

                <h3 className="text-slate-400 text-sm font-medium mb-1">{title}</h3>
                <p className="text-3xl font-bold text-white tracking-tight">{value}</p>
            </div>
        </div>
    );
};

export default DashboardCard;
