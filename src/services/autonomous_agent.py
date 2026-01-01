from typing import Dict, List, Optional
from datetime import datetime, timedelta
import schedule
import time
from dataclasses import dataclass
from enum import Enum


class InterventionType(Enum):
    """Types of autonomous interventions"""
    CHECK_IN = "check_in"                    # Regular wellness check
    PREVENTIVE = "preventive"                # Before predicted stress
    FOLLOW_UP = "follow_up"                  # After difficult conversation
    CELEBRATION = "celebration"              # Acknowledge progress
    GOAL_REMINDER = "goal_reminder"          # Remind about goals
    PATTERN_ALERT = "pattern_alert"          # Alert about negative pattern
    RESOURCE_SUGGESTION = "resource"         # Suggest helpful content


@dataclass
class InterventionTrigger:
    """Defines when to trigger an intervention"""
    type: InterventionType
    condition: str  # Python expression to evaluate
    message_template: str
    priority: int  # 1-5, higher = more urgent
    cooldown_hours: int  # Minimum hours between same type


class AutonomousAgent:
    """
    AUTONOMOUS AI AGENT
    
    What makes it autonomous:
    1. Initiates conversations (not just responds)
    2. Predicts needs before user asks
    3. Tracks patterns and intervenes proactively
    4. Learns optimal interaction times
    5. Adapts behavior based on user response
    
    Examples of autonomous behavior:
    - "Hey! I noticed you haven't checked in today. Everything okay? 💙"
    - "Last Monday you mentioned feeling stressed. How's this Monday treating you?"
    - "You've been doing great with your meditation goal! 5 days in a row! 🎉"
    - "I noticed you tend to feel down on Sunday evenings. Want to prepare together?"
    """
    
    def __init__(self, user_id: str, memory_service, context_service):
        self.user_id = user_id
        self.memory_service = memory_service
        self.context_service = context_service
        
        # Track last interventions to avoid spam
        self.last_interventions = {}
        
        # Define intervention rules
        self.intervention_rules = self._define_intervention_rules()
        
        print(f"🤖 Autonomous agent activated for user {user_id}")
    
    def check_for_interventions(self) -> Optional[Dict]:
        """
        Check if any intervention should be triggered
        
        Called periodically (e.g., every hour)
        
        Returns intervention message if triggered, None otherwise
        """
        now = datetime.now()
        
        # Get user context
        patterns = self.memory_service.detect_patterns()
        user_profile = self.memory_service.user_profile
        emotional_trend = self.memory_service._analyze_emotional_trend()
        
        # Check each intervention rule
        for rule in self.intervention_rules:
            # Check cooldown
            if not self._check_cooldown(rule, now):
                continue
            
            # Evaluate condition
            if self._evaluate_condition(rule.condition, patterns, user_profile, emotional_trend):
                # Trigger intervention!
                message = self._generate_intervention_message(rule, patterns, user_profile)
                
                # Record intervention
                self.last_interventions[rule.type] = now
                
                return {
                    'type': rule.type.value,
                    'message': message,
                    'priority': rule.priority,
                    'timestamp': now.isoformat()
                }
        
        return None
    
    def schedule_optimal_checkin_time(self) -> str:
        """
        Learn optimal time to check in based on user behavior
        
        Analyzes:
        - When user is most active
        - When user is most receptive
        - Avoids busy times (work hours, sleep time)
        """
        conversations = self.memory_service.conversation_memory
        
        if len(conversations) < 5:
            # Not enough data, use default
            return "09:00"  # Morning check-in
        
        # Analyze conversation times
        hour_activity = {}
        for conv in conversations:
            timestamp = datetime.fromisoformat(conv['timestamp'])
            hour = timestamp.hour
            
            if hour not in hour_activity:
                hour_activity[hour] = 0
            hour_activity[hour] += 1
        
        # Find most active hours
        sorted_hours = sorted(hour_activity.items(), key=lambda x: x[1], reverse=True)
        
        # Prefer morning or evening, avoid late night and early morning
        for hour, count in sorted_hours:
            if 8 <= hour <= 10 or 18 <= hour <= 21:
                return f"{hour:02d}:00"
        
        # Default fallback
        return "09:00"
    
    def generate_progress_summary(self) -> str:
        """
        Generate weekly progress summary
        
        Example:
        "Hey! 🌟 Your week in review:
        - You opened up 7 times this week (that takes courage!)
        - Your mood improved by 25% compared to last week 📈
        - You mentioned meditation 3 times - it seems to help you!
        - One challenge: Mondays are still tough. Let's work on that next week.
        
        What would you like to focus on this coming week?"
        """
        # Get emotional timeline
        last_week = datetime.now() - timedelta(days=7)
        recent_emotions = [
            e for e in self.memory_service.emotional_timeline
            if datetime.fromisoformat(e['timestamp']) > last_week
        ]
        
        if not recent_emotions:
            return "Let's start tracking your progress this week! How are you feeling today? 💙"
        
        # Calculate stats
        num_conversations = len(recent_emotions)
        
        # Mood trend
        emotion_scores = {
            'joy': 1, 'trust': 1, 'anticipation': 0.5,
            'sadness': -1, 'anger': -1, 'fear': -1, 'disgust': -1
        }
        
        avg_score = sum(emotion_scores.get(e['emotion'], 0) for e in recent_emotions) / len(recent_emotions)
        
        # Previous week comparison
        prev_week_start = last_week - timedelta(days=7)
        prev_emotions = [
            e for e in self.memory_service.emotional_timeline
            if prev_week_start < datetime.fromisoformat(e['timestamp']) <= last_week
        ]
        
        if prev_emotions:
            prev_avg = sum(emotion_scores.get(e['emotion'], 0) for e in prev_emotions) / len(prev_emotions)
            improvement = ((avg_score - prev_avg) / abs(prev_avg)) * 100 if prev_avg != 0 else 0
        else:
            improvement = 0
        
        # Positive activities mentioned
        coping = self.memory_service.user_profile['coping_mechanisms']
        top_coping = sorted(coping.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Challenges (triggers)
        triggers = self.memory_service.user_profile['triggers']
        top_triggers = sorted(triggers.items(), key=lambda x: x[1], reverse=True)[:2]
        
        # Generate summary
        summary = f"""🌟 **Your Week in Review**

✨ **Engagement**: You opened up {num_conversations} times this week. That takes courage, and I'm proud of you!

"""
        
        if improvement > 10:
            summary += f"📈 **Mood Trend**: Your overall mood improved by {improvement:.0f}% compared to last week! 🎉\n\n"
        elif improvement < -10:
            summary += f"📉 **Mood Trend**: This week was tougher ({improvement:.0f}%). I'm here for you. Let's talk about it. 💙\n\n"
        else:
            summary += f"📊 **Mood Trend**: Your mood was stable this week. That's good! 😊\n\n"
        
        if top_coping:
            summary += "💪 **What's Helping**: You mentioned:\n"
            for activity, count in top_coping[:2]:
                summary += f"   - {activity.title()} ({count} times) - Keep this up!\n"
            summary += "\n"
        
        if top_triggers:
            summary += "⚠️ **Challenges**: You've been dealing with:\n"
            for trigger, count in top_triggers:
                summary += f"   - {trigger.title()} - Let's work on coping strategies for this\n"
            summary += "\n"
        
        summary += "🎯 **Looking Ahead**: What would you like to focus on this coming week?"
        
        return summary
    
    def suggest_preventive_action(self, predicted_situation: str) -> str:
        """
        Suggest preventive actions before predicted stress
        
        Example:
        Detected pattern: User gets stressed every Monday morning
        
        Intervention (Sunday evening):
        "Hey! 👋 I know Mondays can be tough for you (you mentioned it before).
        
        Want to prepare together? We could:
        1. Plan your Monday schedule 📅
        2. Do a relaxing breathing exercise 🧘
        3. Set a positive intention for the week ✨
        
        Which sounds helpful?"
        """
        # Templates for different situations
        preventive_templates = {
            'monday_stress': """Hey! 👋 I know Mondays can be tough for you.

Want to prepare together? We could:
1. Plan your Monday morning routine 📅
2. Do a quick relaxation exercise 🧘
3. Set a positive intention for the week ✨

Which sounds helpful?""",
            
            'exam_anxiety': """I see you have an exam coming up! 📚

Let's prepare your mindset together:
1. Review what worked during your last exam preparation
2. Practice anxiety-reducing techniques
3. Create a realistic study schedule

Want to start?""",
            
            'social_event': """You mentioned a social event coming up. I know social situations can feel overwhelming sometimes.

Let's prepare:
1. Practice conversation starters
2. Plan self-care for before/after
3. Identify your "escape plan" if you need a break

Sound good?""",
        }
        
        return preventive_templates.get(predicted_situation, 
            "I'm sensing you might need some extra support soon. Want to talk about what's coming up? 💙")
    
    def _define_intervention_rules(self) -> List[InterventionTrigger]:
        """
        Define rules for when to intervene autonomously
        """
        return [
            # Daily check-in (if user hasn't messaged today)
            InterventionTrigger(
                type=InterventionType.CHECK_IN,
                condition="no_message_today",
                message_template="Hey! 👋 Haven't heard from you today. How are you doing? 💙",
                priority=2,
                cooldown_hours=24
            ),
            
            # Deteriorating mood pattern
            InterventionTrigger(
                type=InterventionType.PATTERN_ALERT,
                condition="emotional_trend == 'deteriorating'",
                message_template="I've noticed you've been feeling down lately. Want to talk about what's been going on? I'm here for you. 💙",
                priority=4,
                cooldown_hours=48
            ),
            
            # Monday pattern (if user struggles on Mondays)
            InterventionTrigger(
                type=InterventionType.PREVENTIVE,
                condition="monday_pattern_detected and is_sunday_evening",
                message_template="Hey! I know Mondays can be challenging for you. Want to prepare together tonight? 🌙",
                priority=3,
                cooldown_hours=168  # Once per week
            ),
            
            # Celebration (improving trend)
            InterventionTrigger(
                type=InterventionType.CELEBRATION,
                condition="emotional_trend == 'improving'",
                message_template="Hey! 🎉 I've been noticing positive changes in your mood this week. That's wonderful! What do you think is helping? ✨",
                priority=2,
                cooldown_hours=72
            ),
            
            # Goal reminder (if user set goals)
            InterventionTrigger(
                type=InterventionType.GOAL_REMINDER,
                condition="has_active_goals and goal_due_soon",
                message_template="Quick reminder about your goal! 🎯 How's it going? Any support needed?",
                priority=1,
                cooldown_hours=48
            ),
            
            # Follow-up after crisis
            InterventionTrigger(
                type=InterventionType.FOLLOW_UP,
                condition="had_crisis_recently",
                message_template="Hi. I've been thinking about you. How are you feeling today? Want to check in? 💙",
                priority=5,  # High priority
                cooldown_hours=12
            ),
            
            # Suggest helpful resource
            InterventionTrigger(
                type=InterventionType.RESOURCE_SUGGESTION,
                condition="recurring_issue_detected",
                message_template="I noticed {issue} has come up a few times. I found a resource that might help. Want to check it out? 📚",
                priority=2,
                cooldown_hours=96
            ),
        ]
    
    def _check_cooldown(self, rule: InterventionTrigger, now: datetime) -> bool:
        """
        Check if enough time has passed since last intervention of this type
        """
        if rule.type not in self.last_interventions:
            return True
        
        last_time = self.last_interventions[rule.type]
        hours_passed = (now - last_time).total_seconds() / 3600
        
        return hours_passed >= rule.cooldown_hours
    
    def _evaluate_condition(self, condition: str, patterns: Dict, 
                           user_profile: Dict, emotional_trend: str) -> bool:
        """
        Evaluate if condition is met for intervention
        
        This is simplified - in production, use proper expression evaluation
        """
        # Get current context
        now = datetime.now()
        conversations_today = [
            c for c in self.memory_service.conversation_memory
            if datetime.fromisoformat(c['timestamp']).date() == now.date()
        ]
        
        # Define context variables for condition evaluation
        context = {
            'no_message_today': len(conversations_today) == 0,
            'emotional_trend': emotional_trend,
            'monday_pattern_detected': self._check_monday_pattern(patterns),
            'is_sunday_evening': now.weekday() == 6 and 18 <= now.hour <= 22,
            'has_active_goals': len(user_profile.get('goals', [])) > 0,
            'goal_due_soon': False,  # TODO: Implement goal tracking
            'had_crisis_recently': self._check_recent_crisis(),
            'recurring_issue_detected': len(user_profile.get('triggers', {})) > 0
        }
        
        # Simple condition matching
        return context.get(condition, False)
    
    def _check_monday_pattern(self, patterns: Dict) -> bool:
        """Check if user has Monday stress pattern"""
        if 'weekly_pattern' not in patterns:
            return False
        
        weekly = patterns['weekly_pattern']
        if 'Monday' in weekly:
            monday_stats = weekly['Monday']
            return monday_stats['negative_count'] > monday_stats['positive_count']
        
        return False
    
    def _check_recent_crisis(self) -> bool:
        """Check if user had crisis in last 24 hours"""
        last_day = datetime.now() - timedelta(hours=24)
        
        recent_conversations = [
            c for c in self.memory_service.conversation_memory
            if datetime.fromisoformat(c['timestamp']) > last_day
        ]
        
        return any(c.get('intent') == 'CRISIS' for c in recent_conversations)
    
    def _generate_intervention_message(self, rule: InterventionTrigger, 
                                      patterns: Dict, user_profile: Dict) -> str:
        """
        Generate personalized intervention message
        """
        # Start with template
        message = rule.message_template
        
        # Personalize based on context
        # (In production, use more sophisticated personalization)
        
        return message


# ============================================
# BACKGROUND SCHEDULER
# ============================================

class InterventionScheduler:
    """
    Schedule autonomous interventions in background
    
    Runs periodic checks and triggers interventions
    """
    
    def __init__(self, agent: AutonomousAgent):
        self.agent = agent
    
    def start(self):
        """
        Start background scheduler
        
        Checks for interventions:
        - Every hour (general check)
        - Specific times for daily check-ins
        """
        # Hourly checks
        schedule.every().hour.do(self._check_interventions)
        
        # Daily morning check-in (learned optimal time)
        optimal_time = self.agent.schedule_optimal_checkin_time()
        schedule.every().day.at(optimal_time).do(self._morning_checkin)
        
        # Weekly progress summary (Sunday evening)
        schedule.every().sunday.at("20:00").do(self._weekly_summary)
        
        print("📅 Intervention scheduler started")
        
        # Run scheduler loop
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _check_interventions(self):
        """Periodic intervention check"""
        intervention = self.agent.check_for_interventions()
        
        if intervention:
            print(f"🤖 Intervention triggered: {intervention['type']}")
            # In production: Send notification to user
            self._send_notification(intervention)
    
    def _morning_checkin(self):
        """Morning check-in"""
        message = "Good morning! 🌅 How are you feeling today?"
        self._send_notification({
            'type': 'check_in',
            'message': message,
            'priority': 2
        })
    
    def _weekly_summary(self):
        """Weekly progress summary"""
        summary = self.agent.generate_progress_summary()
        self._send_notification({
            'type': 'progress_summary',
            'message': summary,
            'priority': 3
        })
    
    def _send_notification(self, intervention: Dict):
        """
        Send notification to user
        
        In production, this would:
        - Send push notification
        - Display in-app message
        - Send email (if user prefers)
        """
        print(f"\n{'='*50}")
        print(f"📬 NOTIFICATION TO USER")
        print(f"Type: {intervention['type']}")
        print(f"Priority: {intervention['priority']}")
        print(f"\n{intervention['message']}")
        print(f"{'='*50}\n")


# ============================================
# USAGE EXAMPLE
# ============================================

if __name__ == "__main__":
    from context_memory_service import ContextMemoryService
    
    # Initialize services
    memory = ContextMemoryService(user_id="demo_user")
    
    # Create autonomous agent
    agent = AutonomousAgent(
        user_id="demo_user",
        memory_service=memory,
        context_service=None  # Would be actual context service
    )
    
    # Check for interventions manually
    intervention = agent.check_for_interventions()
    
    if intervention:
        print("Intervention triggered!")
        print(intervention['message'])
    else:
        print("No intervention needed right now")
    
    # Generate weekly summary
    summary = agent.generate_progress_summary()
    print("\n" + summary)
    
    # Start scheduler (in production)
    # scheduler = InterventionScheduler(agent)
    # scheduler.start()