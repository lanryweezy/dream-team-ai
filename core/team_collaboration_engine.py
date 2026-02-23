"""
Team Collaboration Engine
Real-time team communication, file sharing, and project coordination
Provides comprehensive collaboration tools with AI assistance
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import statistics
import uuid

from core.company_blueprint_dataclass import CompanyBlueprint
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

class MessageType(Enum):
    TEXT = "text"
    FILE = "file"
    IMAGE = "image"
    LINK = "link"
    TASK_UPDATE = "task_update"
    MEETING_INVITE = "meeting_invite"
    ANNOUNCEMENT = "announcement"

class ChannelType(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    DIRECT_MESSAGE = "direct_message"
    PROJECT = "project"
    DEPARTMENT = "department"

class MeetingStatus(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class FileType(Enum):
    DOCUMENT = "document"
    SPREADSHEET = "spreadsheet"
    PRESENTATION = "presentation"
    IMAGE = "image"
    VIDEO = "video"
    CODE = "code"
    OTHER = "other"

@dataclass
class TeamMember:
    """Team member profile for collaboration"""
    member_id: str
    name: str
    email: str
    role: str
    department: str
    
    # Status and availability
    status: str = "online"  # online, away, busy, offline
    status_message: Optional[str] = None
    timezone: str = "UTC"
    
    # Collaboration preferences
    notification_preferences: Dict[str, bool] = field(default_factory=lambda: {
        "mentions": True,
        "direct_messages": True,
        "channel_messages": False,
        "file_shares": True,
        "meeting_invites": True
    })
    
    # Activity tracking
    last_active: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    total_messages: int = 0
    files_shared: int = 0
    meetings_attended: int = 0
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class Message:
    """Chat message with rich content support"""
    message_id: str
    channel_id: str
    sender_id: str
    
    # Content
    content: str
    message_type: MessageType = MessageType.TEXT
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    
    # Threading and replies
    thread_id: Optional[str] = None
    reply_to: Optional[str] = None
    replies_count: int = 0
    
    # Reactions and engagement
    reactions: Dict[str, List[str]] = field(default_factory=dict)  # emoji -> user_ids
    mentions: List[str] = field(default_factory=list)  # mentioned user_ids
    
    # AI insights
    ai_sentiment: Optional[str] = None  # positive, neutral, negative
    ai_priority: Optional[str] = None  # low, medium, high
    ai_topics: List[str] = field(default_factory=list)
    
    # Metadata
    edited_at: Optional[str] = None
    deleted_at: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class Channel:
    """Communication channel for team collaboration"""
    channel_id: str
    name: str
    description: str
    channel_type: ChannelType
    
    # Membership
    members: List[str] = field(default_factory=list)  # member_ids
    admins: List[str] = field(default_factory=list)  # member_ids
    creator_id: Optional[str] = None
    
    # Settings
    is_archived: bool = False
    is_read_only: bool = False
    retention_days: Optional[int] = None
    
    # Activity tracking
    message_count: int = 0
    last_message_at: Optional[str] = None
    
    # AI insights
    ai_activity_score: float = 0.0  # 0-10
    ai_engagement_level: str = "medium"  # low, medium, high
    ai_topics: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class SharedFile:
    """Shared file with collaboration features"""
    file_id: str
    name: str
    file_type: FileType
    size_bytes: int
    
    # Storage and access
    file_path: str
    download_url: Optional[str] = None
    preview_url: Optional[str] = None
    
    # Ownership and sharing
    owner_id: str
    shared_with: List[str] = field(default_factory=list)  # member_ids
    channel_id: Optional[str] = None
    
    # Collaboration
    version: int = 1
    comments: List[Dict[str, Any]] = field(default_factory=list)
    collaborators: List[str] = field(default_factory=list)
    
    # Activity tracking
    download_count: int = 0
    view_count: int = 0
    last_accessed: Optional[str] = None
    
    # AI insights
    ai_content_summary: Optional[str] = None
    ai_tags: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class Meeting:
    """Team meeting with collaboration features"""
    meeting_id: str
    title: str
    description: str
    
    # Scheduling
    start_time: str
    end_time: str
    timezone: str = "UTC"
    status: MeetingStatus = MeetingStatus.SCHEDULED
    
    # Participants
    organizer_id: str
    attendees: List[str] = field(default_factory=list)  # member_ids
    optional_attendees: List[str] = field(default_factory=list)
    
    # Meeting details
    location: Optional[str] = None
    meeting_url: Optional[str] = None
    agenda: List[str] = field(default_factory=list)
    
    # Collaboration
    notes: str = ""
    action_items: List[Dict[str, Any]] = field(default_factory=list)
    recordings: List[str] = field(default_factory=list)
    
    # AI insights
    ai_meeting_summary: Optional[str] = None
    ai_key_decisions: List[str] = field(default_factory=list)
    ai_follow_ups: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class Workspace:
    """Collaborative workspace for projects"""
    workspace_id: str
    name: str
    description: str
    
    # Organization
    project_id: Optional[str] = None
    department: Optional[str] = None
    
    # Membership
    members: List[str] = field(default_factory=list)
    admins: List[str] = field(default_factory=list)
    
    # Resources
    channels: List[str] = field(default_factory=list)  # channel_ids
    files: List[str] = field(default_factory=list)  # file_ids
    meetings: List[str] = field(default_factory=list)  # meeting_ids
    
    # Settings
    is_public: bool = True
    is_archived: bool = False
    
    # AI insights
    ai_productivity_score: float = 0.0  # 0-10
    ai_collaboration_health: str = "good"  # poor, fair, good, excellent
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class TeamCollaborationEngine:
    """
    Comprehensive team collaboration system that provides:
    - Real-time messaging and communication
    - File sharing and collaborative editing
    - Meeting scheduling and management
    - Workspace organization
    - AI-powered collaboration insights
    """
    
    def __init__(self):
        self.llm_manager = LLMManager()
        
        # Data storage
        self.team_members: Dict[str, TeamMember] = {}
        self.channels: Dict[str, Channel] = {}
        self.messages: Dict[str, Message] = {}
        self.shared_files: Dict[str, SharedFile] = {}
        self.meetings: Dict[str, Meeting] = {}
        self.workspaces: Dict[str, Workspace] = {}
        
        # Real-time connections (simplified for demo)
        self.active_connections: Dict[str, List[str]] = {}  # member_id -> connection_ids
        
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample collaboration data"""
        
        # Sample team members
        sample_members = [
            TeamMember(
                member_id="tm_001",
                name="Sarah Chen",
                email="sarah@company.com",
                role="Product Manager",
                department="Product",
                status="online",
                status_message="Working on Q4 roadmap",
                total_messages=245,
                files_shared=18,
                meetings_attended=32
            ),
            TeamMember(
                member_id="tm_002",
                name="Alex Rodriguez",
                email="alex@company.com",
                role="Senior Engineer",
                department="Engineering",
                status="busy",
                status_message="Deep work - coding session",
                total_messages=189,
                files_shared=12,
                meetings_attended=28
            ),
            TeamMember(
                member_id="tm_003",
                name="Maya Patel",
                email="maya@company.com",
                role="Marketing Manager",
                department="Marketing",
                status="online",
                total_messages=312,
                files_shared=25,
                meetings_attended=45
            ),
            TeamMember(
                member_id="tm_004",
                name="David Kim",
                email="david@company.com",
                role="UX Designer",
                department="Design",
                status="away",
                status_message="In design review",
                total_messages=156,
                files_shared=22,
                meetings_attended=38
            ),
            TeamMember(
                member_id="tm_005",
                name="Lisa Wang",
                email="lisa@company.com",
                role="Data Scientist",
                department="Engineering",
                status="online",
                status_message="Analyzing user behavior data",
                total_messages=98,
                files_shared=15,
                meetings_attended=24
            )
        ]
        
        for member in sample_members:
            self.team_members[member.member_id] = member
        
        # Sample channels
        sample_channels = [
            Channel(
                channel_id="ch_001",
                name="general",
                description="General company discussions",
                channel_type=ChannelType.PUBLIC,
                members=["tm_001", "tm_002", "tm_003", "tm_004", "tm_005"],
                creator_id="tm_001",
                message_count=1247,
                ai_activity_score=8.5,
                ai_engagement_level="high",
                ai_topics=["company updates", "announcements", "casual chat"]
            ),
            Channel(
                channel_id="ch_002",
                name="product-team",
                description="Product team coordination",
                channel_type=ChannelType.PROJECT,
                members=["tm_001", "tm_002", "tm_004"],
                admins=["tm_001"],
                creator_id="tm_001",
                message_count=892,
                ai_activity_score=9.2,
                ai_engagement_level="high",
                ai_topics=["feature planning", "user feedback", "roadmap discussions"]
            ),
            Channel(
                channel_id="ch_003",
                name="engineering",
                description="Engineering team discussions",
                channel_type=ChannelType.DEPARTMENT,
                members=["tm_002", "tm_005"],
                admins=["tm_002"],
                creator_id="tm_002",
                message_count=654,
                ai_activity_score=7.8,
                ai_engagement_level="medium",
                ai_topics=["technical discussions", "code reviews", "architecture"]
            ),
            Channel(
                channel_id="ch_004",
                name="marketing-campaigns",
                description="Marketing campaign coordination",
                channel_type=ChannelType.DEPARTMENT,
                members=["tm_003", "tm_001"],
                admins=["tm_003"],
                creator_id="tm_003",
                message_count=423,
                ai_activity_score=8.0,
                ai_engagement_level="medium",
                ai_topics=["campaign planning", "content strategy", "analytics"]
            )
        ]
        
        for channel in sample_channels:
            self.channels[channel.channel_id] = channel
        
        # Sample messages
        sample_messages = [
            Message(
                message_id="msg_001",
                channel_id="ch_001",
                sender_id="tm_001",
                content="Good morning team! 🌅 Ready for another productive week. Let's crush our Q4 goals!",
                message_type=MessageType.TEXT,
                reactions={"👍": ["tm_002", "tm_003"], "🚀": ["tm_004", "tm_005"]},
                ai_sentiment="positive",
                ai_priority="medium",
                ai_topics=["motivation", "goals"]
            ),
            Message(
                message_id="msg_002",
                channel_id="ch_002",
                sender_id="tm_002",
                content="The new analytics dashboard is ready for testing. I've deployed it to staging environment.",
                message_type=MessageType.TEXT,
                mentions=["tm_001", "tm_004"],
                ai_sentiment="neutral",
                ai_priority="high",
                ai_topics=["development", "testing", "deployment"]
            ),
            Message(
                message_id="msg_003",
                channel_id="ch_002",
                sender_id="tm_004",
                content="Great work Alex! I'll start the UX testing this afternoon. The new interface looks amazing! 🎨",
                message_type=MessageType.TEXT,
                reply_to="msg_002",
                reactions={"🎉": ["tm_001", "tm_002"]},
                ai_sentiment="positive",
                ai_priority="medium",
                ai_topics=["testing", "design", "feedback"]
            ),
            Message(
                message_id="msg_004",
                channel_id="ch_003",
                sender_id="tm_005",
                content="I've completed the user behavior analysis. The conversion funnel shows a 23% improvement after the recent changes.",
                message_type=MessageType.TEXT,
                attachments=[{
                    "type": "file",
                    "name": "conversion_analysis_q4.pdf",
                    "size": "2.3MB",
                    "url": "/files/conversion_analysis_q4.pdf"
                }],
                ai_sentiment="positive",
                ai_priority="high",
                ai_topics=["analytics", "conversion", "performance"]
            ),
            Message(
                message_id="msg_005",
                channel_id="ch_004",
                sender_id="tm_003",
                content="Our LinkedIn campaign is performing exceptionally well! 📈 CTR is up 45% compared to last month.",
                message_type=MessageType.TEXT,
                reactions={"🔥": ["tm_001"], "📊": ["tm_005"]},
                ai_sentiment="positive",
                ai_priority="high",
                ai_topics=["marketing", "performance", "social media"]
            )
        ]
        
        for message in sample_messages:
            self.messages[message.message_id] = message
        
        # Sample shared files
        sample_files = [
            SharedFile(
                file_id="file_001",
                name="Q4_Product_Roadmap.pdf",
                file_type=FileType.DOCUMENT,
                size_bytes=5242880,  # 5MB
                file_path="/shared/documents/Q4_Product_Roadmap.pdf",
                owner_id="tm_001",
                shared_with=["tm_002", "tm_003", "tm_004"],
                channel_id="ch_002",
                download_count=12,
                view_count=28,
                ai_content_summary="Comprehensive product roadmap for Q4 2025 including feature priorities, timeline, and resource allocation",
                ai_tags=["roadmap", "product", "planning", "Q4"]
            ),
            SharedFile(
                file_id="file_002",
                name="User_Research_Findings.pptx",
                file_type=FileType.PRESENTATION,
                size_bytes=15728640,  # 15MB
                file_path="/shared/presentations/User_Research_Findings.pptx",
                owner_id="tm_004",
                shared_with=["tm_001", "tm_003"],
                download_count=8,
                view_count=15,
                ai_content_summary="User research insights from 50+ customer interviews revealing key pain points and feature requests",
                ai_tags=["research", "users", "insights", "interviews"]
            ),
            SharedFile(
                file_id="file_003",
                name="Marketing_Campaign_Assets.zip",
                file_type=FileType.OTHER,
                size_bytes=52428800,  # 50MB
                file_path="/shared/marketing/Marketing_Campaign_Assets.zip",
                owner_id="tm_003",
                shared_with=["tm_001", "tm_004"],
                channel_id="ch_004",
                download_count=6,
                view_count=10,
                ai_content_summary="Complete marketing asset package including graphics, copy, and campaign materials",
                ai_tags=["marketing", "assets", "campaign", "graphics"]
            )
        ]
        
        for file in sample_files:
            self.shared_files[file.file_id] = file
        
        # Sample meetings
        sample_meetings = [
            Meeting(
                meeting_id="meet_001",
                title="Weekly Product Sync",
                description="Weekly product team synchronization and planning meeting",
                start_time="2025-10-01T14:00:00Z",
                end_time="2025-10-01T15:00:00Z",
                organizer_id="tm_001",
                attendees=["tm_001", "tm_002", "tm_004"],
                agenda=[
                    "Review last week's progress",
                    "Discuss upcoming features",
                    "Address blockers and dependencies",
                    "Plan next week's priorities"
                ],
                ai_meeting_summary="Productive sync covering Q4 feature development progress and timeline adjustments",
                ai_key_decisions=["Prioritize mobile optimization", "Delay advanced analytics by 1 week"],
                ai_follow_ups=["Alex to update API documentation", "David to finalize mobile mockups"]
            ),
            Meeting(
                meeting_id="meet_002",
                title="Q4 Strategy Review",
                description="Quarterly strategy review and planning session",
                start_time="2025-10-03T10:00:00Z",
                end_time="2025-10-03T12:00:00Z",
                organizer_id="tm_001",
                attendees=["tm_001", "tm_002", "tm_003", "tm_004", "tm_005"],
                agenda=[
                    "Q3 performance review",
                    "Q4 objectives and key results",
                    "Resource allocation",
                    "Risk assessment and mitigation"
                ],
                status=MeetingStatus.SCHEDULED
            ),
            Meeting(
                meeting_id="meet_003",
                title="Design System Workshop",
                description="Collaborative workshop to establish design system guidelines",
                start_time="2025-10-02T13:00:00Z",
                end_time="2025-10-02T16:00:00Z",
                organizer_id="tm_004",
                attendees=["tm_004", "tm_001", "tm_002"],
                optional_attendees=["tm_003"],
                agenda=[
                    "Review current design patterns",
                    "Define component library structure",
                    "Establish design tokens",
                    "Create implementation guidelines"
                ],
                status=MeetingStatus.SCHEDULED
            )
        ]
        
        for meeting in sample_meetings:
            self.meetings[meeting.meeting_id] = meeting
        
        # Sample workspaces
        sample_workspaces = [
            Workspace(
                workspace_id="ws_001",
                name="Q4 Product Launch",
                description="Collaborative workspace for Q4 product launch coordination",
                project_id="proj_001",
                members=["tm_001", "tm_002", "tm_003", "tm_004"],
                admins=["tm_001"],
                channels=["ch_002"],
                files=["file_001", "file_002"],
                meetings=["meet_001", "meet_002"],
                ai_productivity_score=8.7,
                ai_collaboration_health="excellent"
            ),
            Workspace(
                workspace_id="ws_002",
                name="Marketing Campaigns",
                description="Marketing team collaboration space",
                department="Marketing",
                members=["tm_003", "tm_001"],
                admins=["tm_003"],
                channels=["ch_004"],
                files=["file_003"],
                ai_productivity_score=7.9,
                ai_collaboration_health="good"
            )
        ]
        
        for workspace in sample_workspaces:
            self.workspaces[workspace.workspace_id] = workspace
    
    async def send_message(self, channel_id: str, sender_id: str, content: str, 
                          message_type: MessageType = MessageType.TEXT,
                          attachments: List[Dict[str, Any]] = None,
                          reply_to: str = None) -> Message:
        """Send a message to a channel"""
        
        try:
            if channel_id not in self.channels:
                raise ValueError(f"Channel {channel_id} not found")
            
            if sender_id not in self.team_members:
                raise ValueError(f"Team member {sender_id} not found")
            
            channel = self.channels[channel_id]
            
            # Check if sender is member of channel
            if sender_id not in channel.members:
                raise ValueError(f"User {sender_id} is not a member of channel {channel_id}")
            
            # Create message
            message = Message(
                message_id=f"msg_{uuid.uuid4().hex[:12]}",
                channel_id=channel_id,
                sender_id=sender_id,
                content=content,
                message_type=message_type,
                attachments=attachments or [],
                reply_to=reply_to
            )
            
            # Extract mentions
            message.mentions = self._extract_mentions(content)
            
            # Generate AI insights
            await self._generate_message_ai_insights(message)
            
            # Store message
            self.messages[message.message_id] = message
            
            # Update channel statistics
            channel.message_count += 1
            channel.last_message_at = message.created_at
            
            # Update sender statistics
            sender = self.team_members[sender_id]
            sender.total_messages += 1
            sender.last_active = message.created_at
            
            # Handle reply threading
            if reply_to and reply_to in self.messages:
                parent_message = self.messages[reply_to]
                parent_message.replies_count += 1
                message.thread_id = parent_message.thread_id or parent_message.message_id
            
            logger.info(f"Message sent: {message.message_id} in channel {channel_id}")
            return message
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise
    
    def _extract_mentions(self, content: str) -> List[str]:
        """Extract user mentions from message content"""
        mentions = []
        
        # Simple mention extraction (looking for @username patterns)
        import re
        mention_pattern = r'@(\w+)'
        matches = re.findall(mention_pattern, content)
        
        for match in matches:
            # Find member by name (simplified)
            for member in self.team_members.values():
                if match.lower() in member.name.lower().replace(' ', ''):
                    mentions.append(member.member_id)
                    break
        
        return mentions
    
    async def _generate_message_ai_insights(self, message: Message):
        """Generate AI insights for a message"""
        
        # Simple sentiment analysis
        positive_words = ['great', 'awesome', 'excellent', 'amazing', 'good', 'love', 'perfect', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'problem', 'issue', 'broken', 'failed']
        
        content_lower = message.content.lower()
        
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count > negative_count:
            message.ai_sentiment = "positive"
        elif negative_count > positive_count:
            message.ai_sentiment = "negative"
        else:
            message.ai_sentiment = "neutral"
        
        # Priority detection
        urgent_indicators = ['urgent', 'asap', 'immediately', 'critical', 'emergency', 'blocker']
        high_indicators = ['important', 'priority', 'deadline', 'review', 'approval']
        
        if any(indicator in content_lower for indicator in urgent_indicators):
            message.ai_priority = "high"
        elif any(indicator in content_lower for indicator in high_indicators):
            message.ai_priority = "medium"
        else:
            message.ai_priority = "low"
        
        # Topic extraction (simplified)
        topics = []
        topic_keywords = {
            'development': ['code', 'bug', 'feature', 'api', 'database', 'deploy'],
            'design': ['ui', 'ux', 'mockup', 'prototype', 'design', 'interface'],
            'marketing': ['campaign', 'social', 'content', 'seo', 'analytics'],
            'meeting': ['meeting', 'sync', 'call', 'discussion', 'agenda'],
            'testing': ['test', 'qa', 'bug', 'issue', 'validation']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                topics.append(topic)
        
        message.ai_topics = topics
    
    async def create_channel(self, name: str, description: str, channel_type: ChannelType,
                           creator_id: str, members: List[str] = None) -> Channel:
        """Create a new communication channel"""
        
        try:
            if creator_id not in self.team_members:
                raise ValueError(f"Creator {creator_id} not found")
            
            channel = Channel(
                channel_id=f"ch_{uuid.uuid4().hex[:8]}",
                name=name,
                description=description,
                channel_type=channel_type,
                creator_id=creator_id,
                members=members or [creator_id],
                admins=[creator_id]
            )
            
            # Store channel
            self.channels[channel.channel_id] = channel
            
            logger.info(f"Channel created: {channel.channel_id}")
            return channel
            
        except Exception as e:
            logger.error(f"Failed to create channel: {e}")
            raise
    
    async def share_file(self, file_name: str, file_type: FileType, file_path: str,
                        owner_id: str, shared_with: List[str] = None,
                        channel_id: str = None) -> SharedFile:
        """Share a file with team members"""
        
        try:
            if owner_id not in self.team_members:
                raise ValueError(f"Owner {owner_id} not found")
            
            # Simulate file size (in real implementation, would get actual size)
            import random
            size_bytes = random.randint(1024, 50 * 1024 * 1024)  # 1KB to 50MB
            
            shared_file = SharedFile(
                file_id=f"file_{uuid.uuid4().hex[:8]}",
                name=file_name,
                file_type=file_type,
                size_bytes=size_bytes,
                file_path=file_path,
                owner_id=owner_id,
                shared_with=shared_with or [],
                channel_id=channel_id
            )
            
            # Generate AI insights
            await self._generate_file_ai_insights(shared_file)
            
            # Store file
            self.shared_files[shared_file.file_id] = shared_file
            
            # Update owner statistics
            owner = self.team_members[owner_id]
            owner.files_shared += 1
            
            logger.info(f"File shared: {shared_file.file_id}")
            return shared_file
            
        except Exception as e:
            logger.error(f"Failed to share file: {e}")
            raise
    
    async def _generate_file_ai_insights(self, shared_file: SharedFile):
        """Generate AI insights for a shared file"""
        
        # Generate summary based on file name and type
        file_type_summaries = {
            FileType.DOCUMENT: "Document containing important information and guidelines",
            FileType.PRESENTATION: "Presentation with key insights and strategic information",
            FileType.SPREADSHEET: "Data analysis and calculations in spreadsheet format",
            FileType.IMAGE: "Visual content including diagrams, screenshots, or graphics",
            FileType.CODE: "Source code files and technical implementation",
            FileType.VIDEO: "Video content for training or demonstration purposes"
        }
        
        shared_file.ai_content_summary = file_type_summaries.get(
            shared_file.file_type, 
            "Shared file containing relevant project information"
        )
        
        # Generate tags based on file name
        name_lower = shared_file.name.lower()
        
        tag_keywords = {
            'roadmap': ['roadmap', 'plan', 'strategy'],
            'research': ['research', 'analysis', 'study', 'findings'],
            'design': ['design', 'mockup', 'wireframe', 'prototype'],
            'marketing': ['marketing', 'campaign', 'promotion', 'social'],
            'technical': ['api', 'code', 'technical', 'architecture'],
            'meeting': ['meeting', 'notes', 'minutes', 'agenda'],
            'report': ['report', 'summary', 'results', 'metrics']
        }
        
        tags = []
        for tag, keywords in tag_keywords.items():
            if any(keyword in name_lower for keyword in keywords):
                tags.append(tag)
        
        shared_file.ai_tags = tags or ['general']
    
    async def schedule_meeting(self, title: str, description: str, start_time: str,
                             end_time: str, organizer_id: str, attendees: List[str],
                             agenda: List[str] = None) -> Meeting:
        """Schedule a team meeting"""
        
        try:
            if organizer_id not in self.team_members:
                raise ValueError(f"Organizer {organizer_id} not found")
            
            # Validate attendees
            for attendee_id in attendees:
                if attendee_id not in self.team_members:
                    raise ValueError(f"Attendee {attendee_id} not found")
            
            meeting = Meeting(
                meeting_id=f"meet_{uuid.uuid4().hex[:8]}",
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
                organizer_id=organizer_id,
                attendees=attendees,
                agenda=agenda or []
            )
            
            # Store meeting
            self.meetings[meeting.meeting_id] = meeting
            
            # Update attendee statistics
            for attendee_id in attendees:
                if attendee_id in self.team_members:
                    self.team_members[attendee_id].meetings_attended += 1
            
            logger.info(f"Meeting scheduled: {meeting.meeting_id}")
            return meeting
            
        except Exception as e:
            logger.error(f"Failed to schedule meeting: {e}")
            raise
    
    async def get_collaboration_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive collaboration dashboard data"""
        
        try:
            current_time = datetime.now(timezone.utc)
            
            # Team activity overview
            total_members = len(self.team_members)
            online_members = len([m for m in self.team_members.values() if m.status == "online"])
            total_messages_today = len([
                msg for msg in self.messages.values()
                if (current_time - datetime.fromisoformat(msg.created_at.replace('Z', '+00:00'))).days == 0
            ])
            
            # Channel statistics
            total_channels = len(self.channels)
            active_channels = len([
                ch for ch in self.channels.values()
                if ch.last_message_at and (current_time - datetime.fromisoformat(ch.last_message_at.replace('Z', '+00:00'))).days <= 7
            ])
            
            # File sharing statistics
            total_files = len(self.shared_files)
            files_shared_today = len([
                f for f in self.shared_files.values()
                if (current_time - datetime.fromisoformat(f.created_at.replace('Z', '+00:00'))).days == 0
            ])
            
            # Meeting statistics
            total_meetings = len(self.meetings)
            upcoming_meetings = len([
                m for m in self.meetings.values()
                if m.status == MeetingStatus.SCHEDULED and datetime.fromisoformat(m.start_time.replace('Z', '+00:00')) > current_time
            ])
            
            # Recent activity
            recent_messages = sorted(
                [msg for msg in self.messages.values()],
                key=lambda x: x.created_at,
                reverse=True
            )[:10]
            
            recent_files = sorted(
                [f for f in self.shared_files.values()],
                key=lambda x: x.created_at,
                reverse=True
            )[:5]
            
            # Team member activity
            team_activity = {}
            for member in self.team_members.values():
                member_messages = [msg for msg in self.messages.values() if msg.sender_id == member.member_id]
                recent_activity = len([
                    msg for msg in member_messages
                    if (current_time - datetime.fromisoformat(msg.created_at.replace('Z', '+00:00'))).days <= 7
                ])
                
                team_activity[member.name] = {
                    "status": member.status,
                    "status_message": member.status_message,
                    "recent_messages": recent_activity,
                    "total_messages": member.total_messages,
                    "files_shared": member.files_shared,
                    "last_active": member.last_active
                }
            
            # Channel engagement
            channel_engagement = {}
            for channel in self.channels.values():
                if channel.channel_type != ChannelType.DIRECT_MESSAGE:
                    channel_messages = [msg for msg in self.messages.values() if msg.channel_id == channel.channel_id]
                    recent_activity = len([
                        msg for msg in channel_messages
                        if (current_time - datetime.fromisoformat(msg.created_at.replace('Z', '+00:00'))).days <= 7
                    ])
                    
                    channel_engagement[channel.name] = {
                        "total_messages": channel.message_count,
                        "recent_activity": recent_activity,
                        "member_count": len(channel.members),
                        "engagement_level": channel.ai_engagement_level,
                        "activity_score": channel.ai_activity_score
                    }
            
            # Upcoming meetings
            upcoming_meetings_list = []
            for meeting in self.meetings.values():
                if meeting.status == MeetingStatus.SCHEDULED:
                    start_time = datetime.fromisoformat(meeting.start_time.replace('Z', '+00:00'))
                    if start_time > current_time:
                        upcoming_meetings_list.append({
                            "meeting_id": meeting.meeting_id,
                            "title": meeting.title,
                            "start_time": meeting.start_time,
                            "organizer": self.team_members.get(meeting.organizer_id, {}).get("name", "Unknown"),
                            "attendee_count": len(meeting.attendees),
                            "has_agenda": len(meeting.agenda) > 0
                        })
            
            # Sort upcoming meetings by start time
            upcoming_meetings_list.sort(key=lambda x: x["start_time"])
            
            dashboard_data = {
                "team_overview": {
                    "total_members": total_members,
                    "online_members": online_members,
                    "messages_today": total_messages_today,
                    "online_percentage": round((online_members / max(total_members, 1)) * 100, 1)
                },
                "communication_stats": {
                    "total_channels": total_channels,
                    "active_channels": active_channels,
                    "total_messages": len(self.messages),
                    "avg_channel_activity": round(statistics.mean([
                        ch.ai_activity_score for ch in self.channels.values()
                        if ch.ai_activity_score > 0
                    ]), 1) if any(ch.ai_activity_score > 0 for ch in self.channels.values()) else 0
                },
                "file_sharing_stats": {
                    "total_files": total_files,
                    "files_today": files_shared_today,
                    "total_downloads": sum(f.download_count for f in self.shared_files.values()),
                    "avg_file_size_mb": round(statistics.mean([
                        f.size_bytes / (1024 * 1024) for f in self.shared_files.values()
                    ]), 1) if self.shared_files else 0
                },
                "meeting_stats": {
                    "total_meetings": total_meetings,
                    "upcoming_meetings": upcoming_meetings,
                    "completed_meetings": len([m for m in self.meetings.values() if m.status == MeetingStatus.COMPLETED]),
                    "avg_meeting_duration": 60  # Simplified
                },
                "recent_messages": [
                    {
                        "message_id": msg.message_id,
                        "content": msg.content[:100] + "..." if len(msg.content) > 100 else msg.content,
                        "sender": self.team_members.get(msg.sender_id, {}).get("name", "Unknown"),
                        "channel": self.channels.get(msg.channel_id, {}).get("name", "Unknown"),
                        "created_at": msg.created_at,
                        "sentiment": msg.ai_sentiment,
                        "priority": msg.ai_priority
                    }
                    for msg in recent_messages
                ],
                "recent_files": [
                    {
                        "file_id": f.file_id,
                        "name": f.name,
                        "type": f.file_type.value,
                        "owner": self.team_members.get(f.owner_id, {}).get("name", "Unknown"),
                        "size_mb": round(f.size_bytes / (1024 * 1024), 1),
                        "created_at": f.created_at,
                        "download_count": f.download_count
                    }
                    for f in recent_files
                ],
                "team_activity": team_activity,
                "channel_engagement": channel_engagement,
                "upcoming_meetings": upcoming_meetings_list[:5],
                "ai_insights": await self._generate_collaboration_insights()
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get collaboration dashboard data: {e}")
            raise
    
    async def _generate_collaboration_insights(self) -> List[str]:
        """Generate AI-powered collaboration insights"""
        
        insights = []
        
        # Analyze team activity
        online_count = len([m for m in self.team_members.values() if m.status == "online"])
        total_count = len(self.team_members)
        
        if online_count / total_count > 0.8:
            insights.append("🟢 High team availability - great time for collaborative work!")
        elif online_count / total_count < 0.4:
            insights.append("🟡 Low team availability - consider async communication")
        
        # Analyze message sentiment
        recent_messages = [
            msg for msg in self.messages.values()
            if (datetime.now(timezone.utc) - datetime.fromisoformat(msg.created_at.replace('Z', '+00:00'))).days <= 1
        ]
        
        if recent_messages:
            positive_messages = len([msg for msg in recent_messages if msg.ai_sentiment == "positive"])
            if positive_messages / len(recent_messages) > 0.6:
                insights.append("😊 Team morale is high based on positive communication patterns")
        
        # Analyze channel activity
        inactive_channels = [
            ch for ch in self.channels.values()
            if not ch.last_message_at or (datetime.now(timezone.utc) - datetime.fromisoformat(ch.last_message_at.replace('Z', '+00:00'))).days > 7
        ]
        
        if inactive_channels:
            insights.append(f"📢 {len(inactive_channels)} channels have been inactive for over a week")
        
        # Analyze file sharing
        recent_files = [
            f for f in self.shared_files.values()
            if (datetime.now(timezone.utc) - datetime.fromisoformat(f.created_at.replace('Z', '+00:00'))).days <= 7
        ]
        
        if len(recent_files) > 10:
            insights.append("📁 High file sharing activity - team is actively collaborating on documents")
        
        # Default insights if none generated
        if not insights:
            insights = [
                "✅ Team collaboration is running smoothly",
                "💡 Consider scheduling regular team sync meetings",
                "🎯 Encourage more cross-team channel participation"
            ]
        
        return insights

# Global team collaboration engine
team_collaboration_engine = TeamCollaborationEngine()