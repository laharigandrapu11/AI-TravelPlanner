from .base_agent import BaseAgent
import random

class BudgetAgent(BaseAgent):
    """Agent responsible for budget analysis and management"""
    
    def __init__(self):
        super().__init__("BudgetAgent")
        self.budget_categories = {
            'flights': 0.4,      # 40% of budget
            'accommodation': 0.3, # 30% of budget
            'activities': 0.15,  # 15% of budget
            'meals': 0.1,        # 10% of budget
            'transportation': 0.05 # 5% of budget
        }
        
    def process(self, data):
        """Main processing method"""
        return self.analyze_budget(data)
    
    def analyze_budget(self, budget_data):
        """Analyze budget and provide recommendations"""
        self.log_info("Analyzing budget")
        
        try:
            # Validate required fields
            required_fields = ['total_budget']
            self.validate_input(budget_data, required_fields)
            
            total_budget = float(budget_data['total_budget'])
            flights = budget_data.get('flights', {})
            hotels = budget_data.get('hotels', {})
            itinerary = budget_data.get('itinerary', {})
            
            # Calculate actual costs
            actual_costs = self._calculate_actual_costs(flights, hotels, itinerary)
            
            # Calculate budget allocation
            budget_allocation = self._calculate_budget_allocation(total_budget)
            
            # Analyze budget performance
            budget_analysis = self._analyze_budget_performance(
                actual_costs, budget_allocation, total_budget
            )
            
            # Generate recommendations
            recommendations = self._generate_budget_recommendations(
                budget_analysis, total_budget
            )
            
            analysis_result = {
                'total_budget': total_budget,
                'actual_costs': actual_costs,
                'budget_allocation': budget_allocation,
                'budget_analysis': budget_analysis,
                'recommendations': recommendations,
                'summary': self._create_budget_summary(budget_analysis)
            }
            
            self.log_info(f"Budget analysis completed. Total cost: ${actual_costs['total']:.2f}")
            return analysis_result
            
        except Exception as e:
            self.log_error(f"Error analyzing budget: {str(e)}")
            raise
    
    def _calculate_actual_costs(self, flights, hotels, itinerary):
        """Calculate actual costs from flights, hotels, and itinerary"""
        costs = {
            'flights': 0,
            'accommodation': 0,
            'activities': 0,
            'meals': 0,
            'transportation': 0,
            'total': 0
        }
        
        # Calculate flight costs
        if flights and flights.get('flight_options'):
            best_flight = flights['flight_options'][0]  # Assume first is best
            costs['flights'] = best_flight.get('total_price', 0)
        
        # Calculate accommodation costs
        if hotels and hotels.get('hotel_options'):
            best_hotel = hotels['hotel_options'][0]  # Assume first is best
            costs['accommodation'] = best_hotel.get('estimated_price', 0)
        
        # Calculate activity and meal costs from itinerary
        if itinerary and itinerary.get('daily_plans'):
            daily_plans = itinerary['daily_plans']
            for day in daily_plans:
                if 'estimated_cost' in day:
                    day_cost = day['estimated_cost']
                    costs['activities'] += day_cost.get('activities', 0)
                    costs['meals'] += day_cost.get('meals', 0)
                    costs['transportation'] += day_cost.get('transportation', 0)
        
        # Calculate total
        costs['total'] = sum(costs.values())
        
        return costs
    
    def _calculate_budget_allocation(self, total_budget):
        """Calculate recommended budget allocation"""
        allocation = {}
        
        for category, percentage in self.budget_categories.items():
            allocation[category] = {
                'recommended': total_budget * percentage,
                'percentage': percentage * 100
            }
        
        return allocation
    
    def _analyze_budget_performance(self, actual_costs, budget_allocation, total_budget):
        """Analyze how well the budget is being used"""
        analysis = {}
        
        for category in self.budget_categories.keys():
            actual = actual_costs.get(category, 0)
            recommended = budget_allocation[category]['recommended']
            
            if recommended > 0:
                percentage_used = (actual / recommended) * 100
                status = self._get_budget_status(percentage_used)
            else:
                percentage_used = 0
                status = 'no_budget'
            
            analysis[category] = {
                'actual': actual,
                'recommended': recommended,
                'percentage_used': percentage_used,
                'status': status,
                'difference': actual - recommended
            }
        
        # Overall analysis
        total_actual = actual_costs['total']
        total_percentage = (total_actual / total_budget) * 100 if total_budget > 0 else 0
        overall_status = self._get_budget_status(total_percentage)
        
        analysis['overall'] = {
            'actual': total_actual,
            'budget': total_budget,
            'percentage_used': total_percentage,
            'status': overall_status,
            'remaining': total_budget - total_actual
        }
        
        return analysis
    
    def _get_budget_status(self, percentage_used):
        """Get budget status based on percentage used"""
        if percentage_used < 80:
            return 'under_budget'
        elif percentage_used <= 100:
            return 'within_budget'
        elif percentage_used <= 120:
            return 'over_budget'
        else:
            return 'significantly_over_budget'
    
    def _generate_budget_recommendations(self, budget_analysis, total_budget):
        """Generate budget recommendations based on analysis"""
        recommendations = []
        
        overall = budget_analysis.get('overall', {})
        remaining = overall.get('remaining', 0)
        status = overall.get('status', 'within_budget')
        
        # Overall budget recommendations
        if status == 'under_budget':
            if remaining > 100:
                recommendations.append({
                    'type': 'suggestion',
                    'category': 'overall',
                    'message': f'You have ${remaining:.2f} remaining. Consider upgrading your accommodation or adding premium activities.',
                    'priority': 'low'
                })
        elif status == 'over_budget':
            recommendations.append({
                'type': 'warning',
                'category': 'overall',
                'message': f'You are ${abs(remaining):.2f} over budget. Consider cost-saving alternatives.',
                'priority': 'high'
            })
        elif status == 'significantly_over_budget':
            recommendations.append({
                'type': 'critical',
                'category': 'overall',
                'message': f'You are significantly over budget by ${abs(remaining):.2f}. Major adjustments needed.',
                'priority': 'critical'
            })
        
        # Category-specific recommendations
        for category, analysis in budget_analysis.items():
            if category == 'overall':
                continue
                
            category_status = analysis.get('status', 'within_budget')
            difference = analysis.get('difference', 0)
            
            if category_status == 'over_budget':
                recommendations.append({
                    'type': 'warning',
                    'category': category,
                    'message': f'{category.title()} is ${difference:.2f} over recommended budget.',
                    'priority': 'medium'
                })
            elif category_status == 'under_budget' and difference < -50:
                recommendations.append({
                    'type': 'suggestion',
                    'category': category,
                    'message': f'{category.title()} is ${abs(difference):.2f} under budget. You could upgrade this category.',
                    'priority': 'low'
                })
        
        return recommendations
    
    def _create_budget_summary(self, budget_analysis):
        """Create a summary of the budget analysis"""
        overall = budget_analysis.get('overall', {})
        
        summary = {
            'total_cost': overall.get('actual', 0),
            'total_budget': overall.get('budget', 0),
            'remaining': overall.get('remaining', 0),
            'status': overall.get('status', 'within_budget'),
            'percentage_used': overall.get('percentage_used', 0)
        }
        
        # Add category breakdown
        category_summary = {}
        for category, analysis in budget_analysis.items():
            if category != 'overall':
                category_summary[category] = {
                    'cost': analysis.get('actual', 0),
                    'percentage': analysis.get('percentage_used', 0),
                    'status': analysis.get('status', 'within_budget')
                }
        
        summary['categories'] = category_summary
        return summary
    
    def optimize_budget(self, trip_data, target_budget):
        """Optimize trip to fit within target budget"""
        self.log_info(f"Optimizing trip for budget: ${target_budget}")
        
        try:
            # This would implement budget optimization logic
            # For now, return basic optimization suggestions
            optimization_suggestions = [
                {
                    'category': 'flights',
                    'suggestion': 'Consider flying on weekdays or off-peak times',
                    'potential_savings': random.uniform(50, 200)
                },
                {
                    'category': 'accommodation',
                    'suggestion': 'Look for package deals or book in advance',
                    'potential_savings': random.uniform(30, 150)
                },
                {
                    'category': 'activities',
                    'suggestion': 'Mix free activities with paid attractions',
                    'potential_savings': random.uniform(20, 100)
                },
                {
                    'category': 'meals',
                    'suggestion': 'Eat at local markets and casual restaurants',
                    'potential_savings': random.uniform(15, 80)
                }
            ]
            
            return {
                'target_budget': target_budget,
                'current_cost': trip_data.get('total_cost', 0),
                'optimization_suggestions': optimization_suggestions,
                'total_potential_savings': sum(s['potential_savings'] for s in optimization_suggestions)
            }
            
        except Exception as e:
            self.log_error(f"Error optimizing budget: {str(e)}")
            raise 